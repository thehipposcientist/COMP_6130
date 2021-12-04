import torch
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from PIL import Image
import inversefed
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--signed', type=bool, default=True)
    parser.add_argument('--boxed', type=bool, default=True)
    parser.add_argument('--max_iterations', type=int, default=4000)
    parser.add_argument('--lr', type=float, default=0.1)
    parser.add_argument('--lr_decay', type=bool, default=True)
    parser.add_argument('--optim', type=str, default='adam')
    parser.add_argument('--restarts', type=int, default=1)
    parsed_args = parser.parse_args()

    config = dict(signed=parsed_args.signed,
                boxed=parsed_args.boxed,
                cost_fn='sim',
                indices='def',
                weights='equal',
                lr=parsed_args.lr,
                optim=parsed_args.optim,
                restarts=parsed_args.restarts,
                max_iterations=parsed_args.max_iterations,
                total_variation=1e-6,
                init='randn',
                filter='none',
                lr_decay=parsed_args.lr_decay,
                scoring_choice='loss')

    arch = 'ConvNet64'
    num_images = 1
    trained_model = False

    setup = inversefed.utils.system_startup()
    defs = inversefed.training_strategy('conservative')

    loss_fn, trainloader, validloader =  inversefed.construct_dataloaders('CIFAR10', defs)

    model, _ = inversefed.construct_model(arch, num_classes=10, num_channels=3)
    model.to(**setup)
    if trained_model:
        epochs = 120
        file = f'{arch}_{epochs}.pth'
        try:
            model.load_state_dict(torch.load(f'models/{file}'))
        except FileNotFoundError:
            inversefed.train(model, loss_fn, trainloader, validloader, defs, setup=setup)
            torch.save(model.state_dict(), f'models/{file}')
    model.eval();

    dm = torch.as_tensor(inversefed.consts.cifar10_mean, **setup)[:, None, None]
    ds = torch.as_tensor(inversefed.consts.cifar10_std, **setup)[:, None, None]

    def plot(tensor):
        tensor = tensor.clone().detach()
        tensor.mul_(ds).add_(dm).clamp_(0, 1)
        if tensor.shape[0] == 1:
            return plt.imshow(tensor[0].permute(1, 2, 0).cpu());
        else:
            fig, axes = plt.subplots(1, tensor.shape[0], figsize=(12, tensor.shape[0]*12))
            for i, im in enumerate(tensor):
                axes[i].imshow(im.permute(1, 2, 0).cpu());

    if num_images == 1:
        ground_truth_image = torch.as_tensor(np.array(Image.open("auto.jpg").resize((32, 32), Image.BICUBIC)) / 255, 
                                            **setup)
        ground_truth = ground_truth_image.permute(2, 0, 1).sub(dm).div(ds).unsqueeze(0).contiguous()
        labels = torch.as_tensor((1,), device=setup['device'])
    else:
        ground_truth, labels = [], []
        idx = 25 # choosen randomly ... just whatever you want
        while len(labels) < num_images:
            img, label = validloader.dataset[idx]
            idx += 1
            if label not in labels:
                labels.append(torch.as_tensor((label,), device=setup['device']))
                ground_truth.append(img.to(**setup))
        ground_truth = torch.stack(ground_truth)
        labels = torch.cat(labels)

    plot(ground_truth);
    print([validloader.dataset.classes[l] for l in labels]);

    model.zero_grad()
    target_loss, _, _ = loss_fn(model(ground_truth), labels)
    input_gradient = torch.autograd.grad(target_loss, model.parameters())
    input_gradient = [grad.detach() for grad in input_gradient]

    rec_machine = inversefed.GradientReconstructor(model, (dm, ds), config, num_images=num_images)
    output, stats = rec_machine.reconstruct(input_gradient, labels, img_shape=(3, 32, 32))

    test_mse = (output.detach() - ground_truth).pow(2).mean()
    feat_mse = (model(output.detach())- model(ground_truth)).pow(2).mean()  
    test_psnr = inversefed.metrics.psnr(output, ground_truth, factor=1/ds)

    plot(output)
    plt.title(f"Rec. loss: {stats['opt']:2.4f} | MSE: {test_mse:2.4f} "
            f"| PSNR: {test_psnr:4.2f} | FMSE: {feat_mse:2.4e} |");

    plt.savefig('auto-recon.jpg')

    data = inversefed.metrics.activation_errors(model, output, ground_truth)

    fig, axes = plt.subplots(2, 3, sharey=False, figsize=(14,8))
    axes[0, 0].semilogy(list(data['se'].values())[:-3])
    axes[0, 0].set_title('SE')
    axes[0, 1].semilogy(list(data['mse'].values())[:-3])
    axes[0, 1].set_title('MSE')
    axes[0, 2].plot(list(data['sim'].values())[:-3])
    axes[0, 2].set_title('Similarity')

    convs = [val for key, val in data['mse'].items() if 'conv' in key]
    axes[1, 0].semilogy(convs)
    axes[1, 0].set_title('MSE - conv layers')
    convs = [val for key, val in data['mse'].items() if 'conv1' in key]
    axes[1, 1].semilogy(convs)
    convs = [val for key, val in data['mse'].items() if 'conv2' in key]
    axes[1, 1].semilogy(convs)
    axes[1, 1].set_title('MSE - conv1 vs conv2 layers')
    bns = [val for key, val in data['mse'].items() if 'bn' in key]
    axes[1, 2].plot(bns)
    axes[1, 2].set_title('MSE - bn layers')
    fig.suptitle('Error between layers');
    fig.savefig('stats.png')
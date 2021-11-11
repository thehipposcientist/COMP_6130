from federated_learning.utils import replace_0_with_2
from federated_learning.utils import replace_5_with_3
from federated_learning.utils import replace_1_with_9
from federated_learning.utils import replace_4_with_6
from federated_learning.utils import replace_1_with_3
from federated_learning.utils import replace_6_with_0
from federated_learning.worker_selection import RandomSelectionStrategy
from federated_learning.arguments import Arguments
from federated_learning.nets import Cifar10CNN
from federated_learning.nets import FashionMNISTCNN
from server import run_exp
from loguru import logger
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch_size', type=int, default=10)
    parser.add_argument('--test_batch_size', type=int, default=1000)
    parser.add_argument('--epochs', type=int, default=10)
    parser.add_argument('--lr', type=float, default=0.01)
    parser.add_argument('--momentum', type=float, default=0.5)
    parser.add_argument('--cuda', type=bool, default=True)
    parser.add_argument('--shuffle', type=bool, default=False)
    parser.add_argument('--log_interval', type=int, default=100)
    parser.add_argument('--stepsize', type=int, default=50)
    parser.add_argument('--gamma', type=float, default=0.5)
    parser.add_argument('--save_model', type=bool, default=False)
    parser.add_argument('--num_workers', type=int, default=50)
    parser.add_argument('--num_poisoned_workers', type=int, default=25)
    parser.add_argument('--dataset', type=str, default='Fashion-MNIST')
    
    args = Arguments(logger)
    parsed_args = parser.parse_args()

    START_EXP_IDX = 3000
    NUM_EXP = 1
    NUM_POISONED_WORKERS = 0
    REPLACEMENT_METHOD = replace_1_with_9
    KWARGS = {
        "NUM_WORKERS_PER_ROUND" : 5
    }
    
    args.batch_size = parsed_args.batch_size
    args.test_batch_size = parsed_args.test_batch_size
    args.epochs = parsed_args.epochs
    args.lr = parsed_args.lr
    args.momentum = parsed_args.momentum
    args.cuda = parsed_args.cuda
    args.shuffle = parsed_args.shuffle
    args.log_interval = parsed_args.log_interval
    args.scheduler_step_size = parsed_args.stepsize
    args.scheduler_gamma = parsed_args.gamma
    args.num_workers = parsed_args.num_workers
    args.num_poisoned_workers = parsed_args.num_poisoned_workers
        
    if parsed_args.dataset == 'CIFAR-10':
        args.train_data_loader_pickle_path = "data_loaders/cifar10/train_data_loader.pickle"
        args.set_test_data_loader_pickle_path = "data_loaders/cifar10/test_data_loader.pickle"
        args.net = Cifar10CNN
    elif parsed_args.dataset == 'Fashion-MNIST':
        args.train_data_loader_pickle_path = "data_loaders/fashion-mnist/train_data_loader.pickle"
        args.set_test_data_loader_pickle_path = "data_loaders/fashion-mnist/test_data_loader.pickle"
        args.net = FashionMNISTCNN
    
    for experiment_id in range(START_EXP_IDX, START_EXP_IDX + NUM_EXP):
        run_exp(REPLACEMENT_METHOD, args.num_poisoned_workers, KWARGS, RandomSelectionStrategy(), experiment_id, args)
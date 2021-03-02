import torch
import torchvision.datasets
import torchvision.transforms as transforms


class TorchLoader(object):
    def __init__(self, dataset_name,
                 train_batch_size=16,
                 test_batch_size=8,
                 data_path=None):
        transform = transforms.Compose([transforms.ToTensor(),
                                        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
        if hasattr(torchvision.datasets, dataset_name):

            train_set = getattr(torchvision.datasets, dataset_name)(root='./data',
                                                                    train=True,
                                                                    download=True,
                                                                    transform=transform)
            self.train_loader = torch.utils.data.DataLoader(train_set,
                                                            batch_size=train_batch_size,
                                                            shuffle=True,
                                                            num_workers=1,
                                                            pin_memory=False)
            test_set = getattr(torchvision.datasets, dataset_name)(root='./data',
                                                                   train=False,
                                                                   download=True,
                                                                   transform=transform)
            self.test_loader = torch.utils.data.DataLoader(test_set,
                                                           batch_size=test_batch_size,
                                                           shuffle=True,
                                                           num_workers=1,
                                                           pin_memory=False)

        else:
            raise ImportError('unknown dataset {}, only torchvision seems not to support'.format(dataset_name))

    def read_train(self):
        images, labels = next(iter(self.train_loader))
        return images.cuda(non_blocking=True), labels.cuda(non_blocking=True)

    def read_test(self):
        images, labels = next(iter(self.test_loader))
        return images.cuda(non_blocking=True), labels.cuda(non_blocking=True)

from matplotlib import transforms
from torch.utils.data import Dataset

# Manages my dataset, can add functions as needed
class MyDataset(Dataset):
    def __init__(self, features, labels, transforms):
        self.features = features
        self.labels = labels
        self.transforms = transforms
        
    
    def __len__(self):
        return len(self.labels)
    
    
    def __getitem__(self, idx):
        if self.transforms:
                return self.transforms(self.features[idx]), self.lables[idx]
            
        return self.features[idx], self.labels[idx]
    
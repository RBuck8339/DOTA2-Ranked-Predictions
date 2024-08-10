from torch.utils.data import Dataset

# Manages my dataset, can add functions as needed
class MyDataset(Dataset):
    def __init__(self, features, labels):
        self.features = features
        self.labels = labels
        
    
    def __len__(self):
        return len(self.labels)
    
    
    def __getitem__(self, idx):
        return self.features[idx], self.labels[idx]
    
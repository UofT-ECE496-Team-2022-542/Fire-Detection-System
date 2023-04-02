from PIL import Image
import torch
from torch.autograd import Variable
import torchvision.transforms as transforms
from torchvision.models.resnet import ResNet, BasicBlock
import torch.nn as nn
import warnings

class ImageClassifier(ResNet):
    def __init__(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            
            super(ImageClassifier, self).__init__(BasicBlock, [2,2,2,2], num_classes=10)

            self.fc = nn.Sequential(
                nn.Linear(512 * BasicBlock.expansion, 64),
                nn.ReLU(),
                nn.Dropout(.2),
                nn.Linear(64, 2),
                nn.LogSoftmax(dim=1)
            )

def init_model(model_path):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        model = ImageClassifier()                         
        model.load_state_dict(torch.load(
            model_path,
            map_location=torch.device('cpu')
        ))
        model.eval()
        return model
        
def forward_pass(model, image_filepath, detailed_response=False):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        image = Image.open(image_filepath)
        test_transforms = transforms.Compose([transforms.Resize(256), transforms.ToTensor(),])
        image_tensor = test_transforms(image).float()
        image_tensor = image_tensor.unsqueeze_(0)
        input = Variable(image_tensor)
        #input = input.to(device)
        output = model(input)
        
        if detailed_response:
            return str(1 + output.data[0][0]) + " FIRE, " + str(1 + output.data[0][1]) + " NO_FIRE"
        else:
            index = output.data.cpu().numpy().argmax()
            if index==0: return "FIRE"
            else: return "NO_FIRE"

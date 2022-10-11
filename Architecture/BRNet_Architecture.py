import torch.nn as nn
import torch
import torch.nn.functional as F
    
class DoubleConv(nn.Module):
    def __init__(self, in_ch, out_ch):
        super(DoubleConv, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(in_ch, out_ch, 3, padding=1), 
            # inception(out_ch),
            # residual_block(out_ch),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_ch, out_ch, 3, padding=1),
            # inception(out_ch),
            # residual_block(out_ch),
            nn.BatchNorm2d(out_ch),
            # nn.Conv2d(88, out_ch, 3, padding=1),
            nn.ReLU(inplace=True))

    def forward(self, x):
        return self.conv(x)

class UNet(nn.Module):
    '''BRNet with 10 layers'''
    def __init__(self, in_ch, out_ch):
        super(UNet, self).__init__()
        self.conv1 = DoubleConv(in_ch, 64)
        self.pool1 = nn.MaxPool2d((2,2))
        self.conv2 = DoubleConv(64, 128)
        self.pool2 = nn.MaxPool2d((2,2))
        self.conv3 = DoubleConv(128, 256)
        self.pool3 = nn.MaxPool2d((2,2))
        self.conv4 = DoubleConv(256, 512)
        self.pool4 = nn.MaxPool2d((2,2))
        self.conv5 = DoubleConv(512, 1024)

        self.up1 = nn.ConvTranspose2d(1024, 512, 2, stride=2)
        self.conv6 = DoubleConv(1024, 512)
        self.up2 = nn.ConvTranspose2d(512, 256, 2, stride=2)
        self.conv7 = DoubleConv(512, 256)
        self.up3 = nn.ConvTranspose2d(256, 128, 2, stride=2)
        self.conv8 = DoubleConv(256, 128)
        self.up4 = nn.ConvTranspose2d(128, 64, 2, stride=2)
        self.conv9 = DoubleConv(128, 64)
        self.conv10 = nn.Conv2d(64, out_ch, 1)

    def forward(self, x):
        c1 = self.conv1(x)
        p1 = self.pool1(c1)
        c2 = self.conv2(p1)
        p2 = self.pool2(c2)
        c3 = self.conv3(p2)
        p3 = self.pool3(c3)
        c4 = self.conv4(p3)
        p4 = self.pool4(c4)
        c5 = self.conv5(p4)
        
        up_1 = self.up1(c5)
        merge1 = torch.cat([up_1, c4], dim=1)
        c6 = self.conv6(merge1)
        up_2 = self.up2(c6)
        merge2 = torch.cat([up_2, c3], dim=1)
        c7 = self.conv7(merge2)
        up_3 = self.up3(c7)
        merge3 = torch.cat([up_3, c2], dim=1)
        c8 = self.conv8(merge3)
        up_4 = self.up4(c8)
        merge4 = torch.cat([up_4, c1], dim=1)
        c9 = self.conv9(merge4)
        c10 = self.conv10(c9)
        return c10

class UNet1(nn.Module):
    '''BRNet with interpolation for upsampling'''
    def __init__(self, in_ch, out_ch):
        super(UNet1, self).__init__()
        self.conv1 = DoubleConv(in_ch, 64)
        self.pool1 = nn.MaxPool2d((2,2))
        self.conv2 = DoubleConv(64, 128)
        self.pool2 = nn.MaxPool2d((2,2))
        self.conv3 = DoubleConv(128, 256)
        self.pool3 = nn.MaxPool2d((2,2))
        self.conv4 = DoubleConv(256, 512)
        self.pool4 = nn.MaxPool2d((2,2))
        self.conv5 = DoubleConv(512, 1024)

        self.upsample = nn.Upsample(scale_factor=2, mode="bicubic")
        self.up1 = nn.Conv2d(1024, 512, 3, padding=1)
        self.conv6 = DoubleConv(1024, 512)
        self.up2 = nn.Conv2d(512, 256, 3, padding=1)
        self.conv7 = DoubleConv(512, 256)
        self.up3 = nn.Conv2d(256, 128, 3, padding=1)
        self.conv8 = DoubleConv(256, 128)
        self.up4 = nn.Conv2d(128, 64, 3, padding=1)
        self.conv9 = DoubleConv(128, 64)
        self.conv10 = nn.Conv2d(64, out_ch, 1)

    def forward(self, x):
        c1 = self.conv1(x)
        p1 = self.pool1(c1)
        c2 = self.conv2(p1)
        p2 = self.pool2(c2)
        c3 = self.conv3(p2)
        p3 = self.pool3(c3)
        c4 = self.conv4(p3)
        p4 = self.pool4(c4)
        c5 = self.conv5(p4)
        
        
        up_1 = self.upsample(c5)
        up_1 = self.up1(up_1)
        merge1 = torch.cat([up_1, c4], dim=1)
        c6 = self.conv6(merge1)
        up_2 = self.upsample(c6)
        up_2 = self.up2(up_2)
        merge2 = torch.cat([up_2, c3], dim=1)
        c7 = self.conv7(merge2)
        up_3 = self.upsample(c7)
        up_3 = self.up3(up_3)
        merge3 = torch.cat([up_3, c2], dim=1)
        c8 = self.conv8(merge3)
        up_4 = self.upsample(c8)
        up_4 = self.up4(up_4)
        merge4 = torch.cat([up_4, c1], dim=1)
        c9 = self.conv9(merge4)
        c10 = self.conv10(c9)
        return c10
    
class UNet_4l(nn.Module):
    '''BRNet with 8 layers'''
    def __init__(self, in_ch, out_ch):
        super(UNet_4l, self).__init__()
        self.conv1 = DoubleConv(in_ch, 64)
        self.pool1 = nn.MaxPool2d((2,2))
        self.conv2 = DoubleConv(64, 128)
        self.pool2 = nn.MaxPool2d((2,2))
        self.conv3 = DoubleConv(128, 256)
        self.pool3 = nn.MaxPool2d((2,2))
        self.conv4 = DoubleConv(256, 512)

        self.up1 = nn.ConvTranspose2d(512, 256, 2, stride=2)
        self.conv6 = DoubleConv(512, 256)
        self.up2 = nn.ConvTranspose2d(256, 128, 2, stride=2)
        self.conv7 = DoubleConv(256, 128)
        self.up3 = nn.ConvTranspose2d(128, 64, 2, stride=2)
        self.conv8 = DoubleConv(128, 64)
        self.conv9 = nn.Conv2d(64, out_ch, 1)

    def forward(self, x):
        c1 = self.conv1(x)
        p1 = self.pool1(c1)
        c2 = self.conv2(p1)
        p2 = self.pool2(c2)
        c3 = self.conv3(p2)
        p3 = self.pool3(c3)
        c4 = self.conv4(p3)
        
        up_1 = self.up1(c4)
        merge1 = torch.cat([up_1, c3], dim=1)
        c5 = self.conv6(merge1)
        up_2 = self.up2(c5)
        merge2 = torch.cat([up_2, c2], dim=1)
        c6 = self.conv7(merge2)
        up_3 = self.up3(c6)
        merge3 = torch.cat([up_3, c1], dim=1)
        c8 = self.conv8(merge3)
        c9 = self.conv9(c8)
        return c9
    
class UNet_6l(nn.Module):

    def __init__(self, in_ch, out_ch):
        super(UNet_6l, self).__init__()
        self.conv1 = DoubleConv(in_ch, 32)
        self.pool1 = nn.MaxPool2d((2,2))
        self.conv2 = DoubleConv(32, 64)
        self.pool2 = nn.MaxPool2d((2,2))
        self.conv3 = DoubleConv(64, 128)
        self.pool3 = nn.MaxPool2d((2,2))
        self.conv4 = DoubleConv(128, 256)
        self.pool4 = nn.MaxPool2d((2,2))
        self.conv5 = DoubleConv(256, 512)
        self.pool5 = nn.MaxPool2d((2,2))
        self.conv6 = DoubleConv(512, 1024)

        self.up1 = nn.ConvTranspose2d(1024, 512, 2, stride=2)
        self.conv7 = DoubleConv(1024, 512)
        self.up2 = nn.ConvTranspose2d(512, 256, 2, stride=2)
        self.conv8 = DoubleConv(512, 256)
        self.up3 = nn.ConvTranspose2d(256, 128, 2, stride=2)
        self.conv9 = DoubleConv(256, 128)
        self.up4 = nn.ConvTranspose2d(128, 64, 2, stride=2)
        self.conv10 = DoubleConv(128, 64)
        self.up5 = nn.ConvTranspose2d(64, 32, 2, stride=2)
        self.conv11 = DoubleConv(64, 32)
        self.conv12 = nn.Conv2d(32, out_ch, 1)

    def forward(self, x):
        c1 = self.conv1(x)
        p1 = self.pool1(c1)
        c2 = self.conv2(p1)
        p2 = self.pool2(c2)
        c3 = self.conv3(p2)
        p3 = self.pool3(c3)
        c4 = self.conv4(p3)
        p4 = self.pool4(c4)
        c5 = self.conv5(p4)
        p5 = self.pool5(c5)
        c6 = self.conv6(p5)
        
        up_1 = self.up1(c6)
        merge1 = torch.cat([up_1, c5], dim=1)
        c7 = self.conv7(merge1)
        up_2 = self.up2(c7)
        merge2 = torch.cat([up_2, c4], dim=1)
        c8 = self.conv8(merge2)
        up_3 = self.up3(c8)
        merge3 = torch.cat([up_3, c3], dim=1)
        c9 = self.conv9(merge3)
        up_4 = self.up4(c9)
        merge4 = torch.cat([up_4, c2], dim=1)
        c10 = self.conv10(merge4)
        up_5 = self.up4(c10)
        merge5 = torch.cat([up_5, c1], dim=1)
        c11 = self.conv11(merge5)
        c12 = self.conv12(c11)
        return c12
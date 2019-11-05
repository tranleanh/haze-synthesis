# Generative Adversarial Networks (GANs)

The repository is for studying GANs.

GAN Diagram (Just a funny explanation):
Generator helps Joker look like an ordinary person in Training Set then Batman (Discriminator) can not distinguish him and other people. Joker can join the ceremony.

<img src="images/new_gan_diagram_LA.png" width="800">

## 1. Deep Convolutional GAN (DCGAN) Testing on MNIST Dataset:

<img src="images/GAN_output.png" width="800">

## 2. Super Resolution GAN (SRGAN) Testing on CelebFaces Attributes (CelebA) Dataset:

<img src="images/srgan_e50.png" width="800">
<img src="images/srgan_e3000.png" width="800">

## 3. How to run:
1. DCGAN:
```bashrc
$ python3 dcgan.py
```
2. SRGAN - Follow the steps at the beginning of srgan.py, then run the command:
```bashrc
$ python3 srgan.py
```

Nov. 2019

Tran Le Anh

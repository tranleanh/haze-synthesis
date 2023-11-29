# Hazy Image Synthesis based on Monodepth and Atmospheric Scattering Model

This project is to synthesize hazy/foggy image using Monodepth and atmospheric scattering model.

Medium article: [Synthesize Hazy/Foggy Image using Monodepth and Atmospheric Scattering Model](https://leanhtrann.medium.com/synthesize-hazy-foggy-image-using-monodepth-and-atmospheric-scattering-model-9850c721b74e)

### Dependencies
- OpenCV
- Matplotlib
- Numpy

### How to Use

#### 1. Generate Depth Map (using Monodepth2)
- An easy-to-use implementation of Monodepth2 can be reached via this [link](https://github.com/nianticlabs/monodepth2)

#### 2. Locate Image Files (optional)
- Put the original (clean) image in the folder "docs"
- Put the generated depth map in the folder "docs"
- Say "fname" is the file name of the clean image, the file name of the generated depth map should be "fname_depth"

#### 3. Generate Hazy Image
- Run notebook: synthesize-haze.ipynb

### Results
- 1st row: original images
- 2nd row: synthesized hazy images with sparse haze
- 3rd row: synthesized hazy images with dense haze
<img src="docs/synthesized-haze-2.png" width="900">

### Citation
```
@article{tran2022novel,
  title={A novel encoder-decoder network with guided transmission map for single image dehazing},
  author={Tran, Le-Anh and Moon, Seokyong and Park, Dong-Chul},
  journal={Procedia Computer Science},
  volume={204},
  pages={682--689},
  year={2022},
  publisher={Elsevier}
}
```


Have fun!

LA Tran

Oct. 2021

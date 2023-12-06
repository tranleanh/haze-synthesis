# Hazy/Dusty Image Synthesis for Driving Scenarios

Paper: Toward Improving Robustness of Object Detectors against Domain Shift (GECOST 2024) [[pdf](https://tranleanh.github.io/assets/pdf/GECOST_2024.pdf)] [[Medium](https://leanhtrann.medium.com/synthesize-hazy-foggy-image-using-monodepth-and-atmospheric-scattering-model-9850c721b74e)]

Authors: [Le-Anh Tran](https://scholar.google.com/citations?user=WzcUE5YAAAAJ&hl=en), [Chung Nguyen Tran](https://scholar.google.com/citations?user=NOlVIV4AAAAJ&hl=en), [Dong-Chul Park](https://scholar.google.com/citations?user=VZUH4sUAAAAJ&hl=en), [Jordi Carrabina](https://scholar.google.com/citations?user=V9-s3BIAAAAJ&hl=ca), [David Castells-Rufas](https://scholar.google.com/citations?user=srfRvBIAAAAJ&hl=en)

<!--- Medium: [Synthesize Hazy/Foggy Image using Monodepth and Atmospheric Scattering Model](https://leanhtrann.medium.com/synthesize-hazy-foggy-image-using-monodepth-and-atmospheric-scattering-model-9850c721b74e) --->
<pre>
<p align="center">
<img src="docs/examples.png" width="900">
</p>
</pre>

### Dependencies

This repo is based on the following project/packages:

- [Monodepth2](https://github.com/nianticlabs/monodepth2)
- Pytorch
- OpenCV

### Setup

- Step 1: Create virtual environment:
  
```
conda create -n hazesynt python=3.6
conda activate hazesynt
```

- Step 2: Install required packages as in [Monodepth2](https://github.com/nianticlabs/monodepth2) or just run this command:

```
pip install -r requirements.txt
```

- Step 3: Download pre-trained model from [Monodepth2](https://github.com/nianticlabs/monodepth2) and place it in 'models/{model_name}', e.g., 'models/mono+stereo_640x192'.

### Image Synthesis

Run the following command to generate synthetic image:

```
python main.py --image_path ./inputs --output_image_path ./outputs --model_name mono+stereo_640x192 --beta 2.0 --airlight 150
```

The values of beta and airlight can be changed (recommended: beta = [1.0,3.0], airlight = [150,255]).

### Citation

If you use this repo in your study, please cite our work:

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

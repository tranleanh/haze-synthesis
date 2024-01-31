# Hazy/Dusty Image Synthesis for Driving Scenarios

[![Paper](https://img.shields.io/badge/Paper-Preprint-lightgrey)](https://tranleanh.github.io/assets/pdf/GECOST_2024.pdf)
[![Blog](https://img.shields.io/badge/Blog-Medium-blue)](https://leanhtrann.medium.com/synthesize-hazy-foggy-image-using-monodepth-and-atmospheric-scattering-model-9850c721b74e)

Paper: Toward Improving Robustness of Object Detectors against Domain Shift (IEEE GECOST 2024)

Authors: [Le-Anh Tran](https://scholar.google.com/citations?user=WzcUE5YAAAAJ&hl=en), [Chung Nguyen Tran](https://scholar.google.com/citations?user=NOlVIV4AAAAJ&hl=en), [Dong-Chul Park](https://scholar.google.com/citations?user=VZUH4sUAAAAJ&hl=en), [Jordi Carrabina](https://scholar.google.com/citations?user=V9-s3BIAAAAJ&hl=ca), [David Castells-Rufas](https://scholar.google.com/citations?user=srfRvBIAAAAJ&hl=en)

<!--- Medium: [Synthesize Hazy/Foggy Image using Monodepth and Atmospheric Scattering Model](https://leanhtrann.medium.com/synthesize-hazy-foggy-image-using-monodepth-and-atmospheric-scattering-model-9850c721b74e) --->
<pre>
<p align="center">
<img src="docs/examples.png" width="900">
</p>
</pre>

## Dependencies

This repo is based on the following project/packages:

- [Monodepth2](https://github.com/nianticlabs/monodepth2)
- Pytorch
- OpenCV

## Setup

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

## Image Synthesis

Run the following command to generate synthetic image:

```
python main.py --image_path ./inputs --output_image_path ./outputs --model_name mono+stereo_640x192 --beta 2.0 --airlight 150
```

The values of beta and airlight can be changed (recommended: beta = [1.0,3.0], airlight = [150,255]).

## Citation

If you feel this repo is helpful for your study, please cite our work:

```bibtex
@inproceedings{tran2024toward,
  title={Toward Improving Robustness of Object Detectors against Domain Shift},
  author={Tran, Le-Anh and Tran, Chung Nguyen and Park, Dong-Chul and Carrabina, Jordi and Castells-Rufas, David},
  booktitle={2024 International Conference on Green Energy, Computing and Sustainable Technology (GECOST)},
  year={2024},
  organization={IEEE}
}
```

Have fun!

LA Tran

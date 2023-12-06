
from __future__ import absolute_import, division, print_function

import os
import sys
import glob
import argparse
import numpy as np
import PIL.Image as pil
import matplotlib as mpl
import matplotlib.cm as cm
import cv2

import torch
from torchvision import transforms, datasets
import networks

def parse_args():

    parser = argparse.ArgumentParser(
        description='Simple testing funtion for Monodepthv2 models.')
    parser.add_argument('--image_path', type=str,
                        help='path to a test image or folder of images', required=True)
    parser.add_argument('--model_name', type=str,
                        help='name of a pretrained model to use',
                        choices=[
                            "mono_640x192",
                            "stereo_640x192",
                            "mono+stereo_640x192",
                            "mono_no_pt_640x192",
                            "stereo_no_pt_640x192",
                            "mono+stereo_no_pt_640x192",
                            "mono_1024x320",
                            "stereo_1024x320",
                            "mono+stereo_1024x320"])
    parser.add_argument('--ext', type=str,
                        help='image extension to search for in folder', default="jpg")
    parser.add_argument("--no_cuda",
                        help='if set, disables CUDA',
                        action='store_true')
    parser.add_argument("--pred_metric_depth",
                        help='if set, predicts metric depth instead of disparity. (This only '
                             'makes sense for stereo-trained KITTI models).',
                        action='store_true')
    parser.add_argument('--output_image_path', type=str,
                        help='path to folder of output images', required=True)
    parser.add_argument('--beta', type=float,
                        help='degree of haze', default=1.)
    parser.add_argument('--airlight', type=float,
                        help='atmospheric light', default=255.)

    return parser.parse_args()


def gen_haze(clean_img, depth_img, beta=1.0, A = 150):

    depth_img_3c = np.zeros_like(clean_img)
    depth_img_3c[:,:,0] = depth_img
    depth_img_3c[:,:,1] = depth_img
    depth_img_3c[:,:,2] = depth_img

    norm_depth_img = depth_img_3c/255
    trans = np.exp(-norm_depth_img*beta)

    hazy = clean_img*trans + A*(1-trans)
    hazy = np.array(hazy, dtype=np.uint8)

    return hazy


def test_simple(args):

    assert args.model_name is not None, \
        "You must specify the --model_name parameter; see README.md for an example"

    if torch.cuda.is_available() and not args.no_cuda:
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")

    if args.pred_metric_depth and "stereo" not in args.model_name:
        print("Warning: The --pred_metric_depth flag only makes sense for stereo-trained KITTI "
              "models. For mono-trained models, output depths will not in metric space.")

    # download_model_if_doesnt_exist(args.model_name)
    model_path = os.path.join("models", args.model_name)
    print("-> Loading model from ", model_path)
    encoder_path = os.path.join(model_path, "encoder.pth")
    depth_decoder_path = os.path.join(model_path, "depth.pth")

    # LOADING PRETRAINED MODEL
    print("   Loading pretrained encoder")
    encoder = networks.ResnetEncoder(18, False)
    loaded_dict_enc = torch.load(encoder_path, map_location=device)

    # EXTRACT THE HEIGHT AND WIDTH OF IMAGE THAT THIS MODEL WAS TRAINED WITH
    feed_height = loaded_dict_enc['height']
    feed_width = loaded_dict_enc['width']
    filtered_dict_enc = {k: v for k, v in loaded_dict_enc.items() if k in encoder.state_dict()}
    encoder.load_state_dict(filtered_dict_enc)
    encoder.to(device)
    encoder.eval()

    print("   Loading pretrained decoder")
    depth_decoder = networks.DepthDecoder(
        num_ch_enc=encoder.num_ch_enc, scales=range(4))

    loaded_dict = torch.load(depth_decoder_path, map_location=device)
    depth_decoder.load_state_dict(loaded_dict)

    depth_decoder.to(device)
    depth_decoder.eval()

    # FINDING INPUT IMAGES
    if os.path.isfile(args.image_path):
        # Only testing on a single image
        paths = [args.image_path]
        output_directory = os.path.dirname(args.image_path)
    elif os.path.isdir(args.image_path):
        # Searching folder for images
        paths = glob.glob(os.path.join(args.image_path, '*.{}'.format(args.ext)))
        output_directory = args.image_path
    else:
        raise Exception("Can not find args.image_path: {}".format(args.image_path))

    print("-> Predicting on {:d} test images".format(len(paths)))

    # CHECK IF OUTPUT FOLDER EXISTS
    if not os.path.isdir(args.output_image_path):
        os.makedirs(args.output_image_path)

    output_dir = args.output_image_path

    # PREDICTING ON EACH IMAGE IN TURN
    with torch.no_grad():
        for idx, image_path in enumerate(paths):

            if image_path.endswith("_disp.jpg"):
                # don't try to predict disparity for a disparity image!
                continue

            # LOAD IMAGE AND PREPROCESS
            input_image = pil.open(image_path).convert('RGB')
            clean_img = input_image.copy()
            original_width, original_height = input_image.size
            input_image = input_image.resize((feed_width, feed_height), pil.LANCZOS)
            input_image = transforms.ToTensor()(input_image).unsqueeze(0)

            # PREDICTION
            input_image = input_image.to(device)
            features = encoder(input_image)
            outputs = depth_decoder(features)

            disp = outputs[("disp", 0)]
            disp_resized = torch.nn.functional.interpolate(
                disp, (original_height, original_width), mode="bilinear", align_corners=False)

            # EXTRACT DEPTH IMAGE
            disp_resized_np = disp_resized.squeeze().cpu().numpy()
            vmax = np.percentile(disp_resized_np, 95)
            normalizer = mpl.colors.Normalize(vmin=disp_resized_np.min(), vmax=vmax)
            mapper = cm.ScalarMappable(norm=normalizer, cmap='magma')
            colormapped_im = (mapper.to_rgba(disp_resized_np)[:, :, :3] * 255).astype(np.uint8)
            im = pil.fromarray(colormapped_im)
            gray_colormapped_im = cv2.cvtColor(colormapped_im, cv2.COLOR_RGB2GRAY)
            inv_gray_colormapped_im = 255 - gray_colormapped_im

            # MAKE HAZY IMAGE: 
            # Change degree of haze by changing 'beta' (recommended value of beta: 0.5 - 3.0)
            # High beta -> Thick haze
            # Low beta -> Sparse haze
            hazy = gen_haze(clean_img, inv_gray_colormapped_im, beta=args.beta, A=args.airlight)

            # SAVE FILES
            output_name = os.path.splitext(os.path.basename(image_path))[0]
            cv2.imwrite(f"{output_dir}/{output_name}_synt.jpg", cv2.cvtColor(hazy, cv2.COLOR_RGB2BGR))

            print("   Processed {:d} of {:d} images".format(idx + 1, len(paths)))

    print(f'-> Done! Find outputs in {output_dir}')

if __name__ == '__main__':
    args = parse_args()
    test_simple(args)

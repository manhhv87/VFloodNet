import argparse
import os
from glob import glob
import torch

from estimation.object_detection import est_by_obj_detection
from estimation.reference_tracking import est_by_reference


def get_parser():
    parser = argparse.ArgumentParser(description='Estimate Water Level')
    parser.add_argument('--test-name', type=str, required=True,
                        help='Name of the test video')
    parser.add_argument('--test-path', type=str, required=True,
                        help='Input image directory.')
    parser.add_argument('--out-dir', default='output/waterlevel',
                        help='A file or directory to save output results.')
    parser.add_argument('--opt', type=str,
                        help='Estimation options. "people", "stopsign", or "ref"')

    return parser.parse_args()


def main(args):

    args.water_mask_dir = os.path.join(
        './output/segs/', args.test_name, 'mask')
    img_list = sorted(glob(os.path.join(args.test_path, '*.jpg')) +
                      glob(os.path.join(args.test_path, '*.png')))
    water_mask_list = sorted(glob(os.path.join(args.water_mask_dir, '*.png')))
    out_dir = os.path.join(args.out_dir, f'{args.test_name}_{args.opt}')
    os.makedirs(out_dir, exist_ok=True)

    record_dir = './records/groundtruth'

    if args.opt in ['people', 'stopsign']:
        est_by_obj_detection(img_list, water_mask_list, out_dir, args.opt)
    elif args.opt == 'ref':
        est_by_reference(img_list, water_mask_list, out_dir,
                         record_dir, args.test_name)
    else:
        raise NotImplementedError(args.opt)


if __name__ == '__main__':

    _args = get_parser()
    print(_args)

    main(_args)

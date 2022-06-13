import cv2
import argparse
import numpy as np
import matplotlib.pyplot as plt


def mmm_stitching(mmm_file, index, rows, columns, overlap, inverted=False):
    mmm_meta = {}

    with open(mmm_file, 'rb') as f:
        nx, ny, nz, mode = np.fromfile(f, np.int32, 4)
        amin, amax, amean = np.fromfile(f, np.float32, 3, offset=60)
        ext_header = np.fromfile(f, np.int32, 1, offset=4)[0]
        if mode == 0:
            p_type = np.int8
        elif mode == 1:
            p_type = np.int16
        elif mode == 2:
            p_type = np.float32

        template_x = nx * overlap // 105
        matching_x = nx * overlap // 95
        template_y = ny * overlap // 105
        matching_y = ny * overlap // 95
        byte_count = np.dtype(p_type).itemsize

        f.seek(928 + int(ext_header) + index * int(nx) * int(ny) * columns * rows * byte_count, 1)

        for i in range(columns):
            row_array = None
            for j in range(rows):
                img_gray = np.fromfile(f, p_type, nx * ny).reshape(ny, nx)

                """
                This seems to work for some but not all micrographs; may have to change depending on the micrographs
                """

                """
                img_gray[img_gray > 255] = 255
                img_gray[img_gray < 0] = 0
                img_gray = np.uint8(img_gray)
                """

                img_gray = (img_gray / 256).astype('uint8')

                if j > 0:
                    template = img_gray[:template_y]
                    full_img = row_array[-matching_y:]

                    match = cv2.matchTemplate(full_img, template, cv2.TM_CCOEFF_NORMED)
                    loc = np.where(np.max(match) == match)

                piece = i * rows + j

                if row_array is None:
                    row_array = img_gray
                    mmm_meta[i] = [nx, {}]
                else:
                    row_array = np.vstack((row_array[:-(template_y - loc[0][0])], img_gray))
                    mmm_meta[i][1][piece - 1] = ny - (template_y - loc[0][0])
                    mmm_meta[i][1][piece] = ny

            if inverted:
                mmm_meta[i][1] = dict(reversed(list(mmm_meta[i][1].items())))

            if i == 0:
                column_array = row_array
            else:
                if (diff := len(row_array) - len(column_array)) > 0:
                    if diff % 2 == 0:
                        column_array = np.pad(column_array, ((diff // 2, diff // 2), (0, 0)), 'constant',
                                              constant_values=0)
                    else:
                        column_array = np.pad(column_array, ((diff // 2, diff // 2 + 1), (0, 0)), 'constant',
                                              constant_values=0)

                template = row_array[:, :template_x]
                full_img = column_array[:, -matching_x:]
                match = cv2.matchTemplate(full_img, template, cv2.TM_CCOEFF_NORMED)
                loc = np.where(np.max(match) == match)
                row_array = np.pad(row_array, ((loc[0][0], len(column_array) - (len(row_array) + loc[0][0])), (0, 0)),
                                   'constant', constant_values=0)
                column_array = np.hstack((column_array[:, :-(matching_x - loc[1][0])], row_array))
                mmm_meta[i - 1][0] -= matching_x - loc[1][0]

    return mmm_meta, column_array


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script for stitching MMM's. Written by Honkit Ng.")

    parser.add_argument('file', help='MMM file location')
    parser.add_argument('rows', help='number of images per rows', type=int)
    parser.add_argument('columns', help='number of images per column', type=int)
    parser.add_argument('overlap', help='%% overlap between individual images', type=int)

    args = parser.parse_args()

    with open(args.file, 'rb') as file:
        nx1, ny1, nz1, mode1 = np.fromfile(file, np.int32, 4)

    image_count = nz1 // args.rows // args.columns

    for img in range(image_count):
        _, mmm = mmm_stitching(args.file, img, args.rows, args.columns, args.overlap)
        mmm = cv2.equalizeHist(mmm)
        # plt.imshow(mmm, cmap='gray')
        # plt.show()
        plt.imsave(f'mmm{img:03d}.tiff', mmm)
        print(f'mmm{img:03d}.tiff generated')

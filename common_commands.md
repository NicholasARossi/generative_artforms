# vpype

vpype read /Volumes/G-RAID/projects/2023_03/moire/complete.svg layout --fit-to-margins 0cm -l a2 write /Volumes/G-RAID/projects/2023_03/moire/vpype_out.svg

IMAGE_DIR = /Volumes/G-RAID/projects/2023_03/moire/

$ vpype \
    read input.svg \
    forlayer \
      write "output_%_name or _lid%.svg" \
    end




# single 
```shell
export IMAGE_DIR=/Volumes/G-RAID/projects/2023_03/moire
vpype read $IMAGE_DIR/complete.svg layout --fit-to-margins 0cm -l a2 write $IMAGE_DIR/vpype_out.svg
```

* split on layer
```shell
vpype \
    read $IMAGE_DIR/complete.svg layout --fit-to-margins 0cm -l a1 \
    forlayer \
      write "$IMAGE_DIR/output_%_name or _lid%.svg" \
    end
```

# pixel art

```shell
export IMAGE_DIR=/Volumes/G-RAID/projects/2023_03/pixelart

vpype pixelart --mode snake --pen-width .35mm $IMAGE_DIR/drinks.png linesort write  $IMAGE_DIR/output.svg
```

# line art

vpype -v -s 42 flow_img -f curl_noise -dfm 1 -nc 0.03
vpype flow_img -nf 6 $IMAGE_DIR/background_contrast.png write $IMAGE_DIR/background_contrast_out.svg show


vpype -v -s 42 flow_img -f curl_noise -nc 0.03 $IMAGE_DIR/background_contrast.png write $IMAGE_DIR/background_contrast_curl.svg show

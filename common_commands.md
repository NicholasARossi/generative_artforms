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
    read $IMAGE_DIR/complete.svg layout --fit-to-margins 0cm -l a2 \
    forlayer \
      write "$IMAGE_DIR/output_%_name or _lid%.svg" \
    end
```


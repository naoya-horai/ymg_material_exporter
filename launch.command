#!/bin/zsh
export SUBSTANCE_PAINTER_PLUGINS_PATH=$SUBSTANCE_PAINTER_PLUGINS_PATH"$(cd "$(dirname "$0")" && pwd)"
open -a "Adobe Substance 3D Painter"

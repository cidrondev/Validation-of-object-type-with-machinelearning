# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

#Added some imports and deleted some
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf
from PIL import Image
import numpy as np
import cv2

"""[summary]
This code is modified from the orginal use to work with our validation programs.
To see the orignal code from the tensorflow authors see below:
https://raw.githubusercontent.com/tensorflow/tensorflow/master/tensorflow/examples/label_image/label_image.py
Author to edits in the code: Daniel Persson 2019-05-22
"""

#This method has not been modified
def load_graph(model_file):
  graph = tf.Graph()
  graph_def = tf.GraphDef()

  with open(model_file, "rb") as f:
    graph_def.ParseFromString(f.read())
  with graph.as_default():
    tf.import_graph_def(graph_def)

  return graph

#This method has not been modified
def read_tensor_from_image_file(file_name,
                                input_height=299,
                                input_width=299,
                                input_mean=0,
                                input_std=255):
  input_name = "file_reader"
  output_name = "normalized"
  file_reader = tf.read_file(file_name, input_name)
  if file_name.endswith(".png"):
    image_reader = tf.image.decode_png(
        file_reader, channels=3, name="png_reader")
  elif file_name.endswith(".gif"):
    image_reader = tf.squeeze(
        tf.image.decode_gif(file_reader, name="gif_reader"))
  elif file_name.endswith(".bmp"):
    image_reader = tf.image.decode_bmp(file_reader, name="bmp_reader")
  else:
    image_reader = tf.image.decode_jpeg(
        file_reader, channels=3, name="jpeg_reader")
  float_caster = tf.cast(image_reader, tf.float32)
  dims_expander = tf.expand_dims(float_caster, 0)
  resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
  normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
  sess = tf.Session()
  result = sess.run(normalized)

  return result

#Removed load_labels method and the arguments

#Modified this part to create a method to make it easier to call from any program
def result(file_name,graph):
  """[summary]
  Returns our results from the google models
  Args:
      file_name ([STR]): [The name of the model]
      graph ([PB]): [The retrained model in pb format]
  """
  
  #Changed to values that are constant
  input_height = 299
  input_width = 299
  input_name = "file_reader"
  output_name = "normalized"
  input_layer = "Placeholder"
  output_layer = "final_result"
  
  #Modify so it only takes in the input we need for the operation
  t = read_tensor_from_image_file(
      file_name,
      input_height=input_height,
      input_width=input_width)

  #This has not been modified
  input_name = "import/" + input_layer
  output_name = "import/" + output_layer
  input_operation = graph.get_operation_by_name(input_name)
  output_operation = graph.get_operation_by_name(output_name)
  
  #This has not been modified
  with tf.Session(graph=graph) as sess:
    results = sess.run(output_operation.outputs[0], {
        input_operation.outputs[0]: t
    })
  results = np.squeeze(results)
  #Removed code here that was related to the outputlabels that was not useful for our need
  return results
#!/usr/bin/python
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

'''Extract Opencl source code into c++ strings, for runtime use.

This file is executed only if .cl files are updated.
It is executed in the ROOT folder of SINGA source repo.
'''
from future.utils import iteritems

distribution = "./src/core/tensor/distribution.cl"
tensormath = "./src/core/tensor/tensor_math_opencl.cl"
im2col = "./src/model/layer/im2col.cl"
pooling = "./src/model/layer/pooling.cl"
files = {"distribution_str": distribution, "tensormath_str": tensormath,
         "im2col_str": im2col, "pooling_str": pooling}


if __name__ == "__main__":
    fullpath = './src/core/device/opencl_func.h'
    with open(fullpath, 'w') as fout:
        fout.write("// This file is auto-generated by tool/opencl/clsrc_to_str."
                   " do not edit manually.\n")
        license = """
/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
"""
        fout.write(license)
        fout.write("#include <string>\n\n")
        fout.write("namespace singa {\n namespace opencl {\n")
        for name, path in iteritems(files):
            with open(path, 'r') as fin:
                src = fin.read()
                src = repr(src)
                src = src[1:-1]
                src = src.replace('\"', '\\"')  # Escape double quotes
                src = src.replace('\\t', '')  # Strip out tabs
                fout.write("const std::string " + name + " = \"")
                fout.write(src)
                fout.write("\";")
        fout.write("\n } //  namespace opencl \n} //  namespace singa")
        fout.close()

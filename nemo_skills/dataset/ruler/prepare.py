# Copyright (c) 2024, NVIDIA CORPORATION.  All rights reserved.
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

import argparse
import json
import os
from pathlib import Path
import glob
from shutil import copyfile
# prepare ruler jsons from steps: 


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--json_folder_path", type=str, default="ruler")
    parser.add_argument('--data_path', type=str, default=None)
    args = parser.parse_args()

    data_dir = Path(__file__).absolute().parent
    data_dir.mkdir(exist_ok=True)

    if args.data_path is not None:
        external_data_dir = Path(args.data_path)
        external_data_dir.mkdir(exist_ok=True)
    
    original_files = [f for f in glob.glob(f"{args.json_folder_path}/**", recursive=True) if os.path.isfile(f)]

    for original_file in original_files:
        print(original_file)
        original_name, task, subset_file = original_file.split("/")[-3].split("_original")[0], original_file.split("/")[-2], original_file.split("/")[-1]
        output_folder = Path(f"../{original_name}_{task}")
        output_folder.mkdir(exist_ok=True)
        output_file = os.path.join(output_folder, subset_file)
        copyfile("./__init__.py", os.path.join(output_folder, "__init__.py"))

        data_fout = None
        if args.data_path is not None:
            external_data_dir = Path(args.data_path) /  f"{original_name}_{task}"
            external_data_dir.mkdir(exist_ok=True)
            output_file = os.path.join(external_data_dir, subset_file)
            copyfile("./__init__.py", os.path.join(external_data_dir, "__init__.py"))

            data_fout = open(output_file, "wt", encoding="utf-8")

        with open(original_file, "r") as fin, open(output_file, "wt", encoding="utf-8") as fout:
            for line in fin:
                original_entry = json.loads(line)
                new_entry = dict(
                    index=original_entry["index"],
                    problem=original_entry["input"],
                    expected_answer=original_entry["outputs"],
                    length=original_entry["length"],
                    assistant_prefix=original_entry['answer_prefix']
                )

                if data_fout is not None:
                    data_fout.write(json.dumps(new_entry) + "\n")
                else:
                    fout.write(json.dumps(new_entry) + "\n")

        if data_fout is not None:
            print(f"Copied data to {output_file}")
            data_fout.close()
        else:
            print(f"Copied data to {output_file}")


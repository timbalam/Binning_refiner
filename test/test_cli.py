
#!/usr/bin/env python

#=======================================================================
# Authors: Tim Lamberton
#
# Unit tests.
#
# Copyright
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License.
# If not, see <http://www.gnu.org/licenses/>.
#=======================================================================

import unittest
import subprocess
import os.path
import os
import shutil
    
data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),'data')
path_to_script = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'bin', 'Binning_refiner')

class Tests(unittest.TestCase):
    
    
    
    def test_binning_refiner(self):
        contigs = [
            '''>seq1
ACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTG
ACTGACTGACTGACTGACTG
''',
            '''>seq2
ACTTACTTACTTACTTACTTACTTACTTACTTACTTACTTACTTACTTACTTACTTACTT
ACTTACTTACTTACTTACTT
''', 
            '''>seq3
GATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATC
GATCGATCGATCGATCGATC
''',
            '''>seq4
GATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATC
GATCGATCGATCGATCGATC
'''
            ]
        bins_1_dir = os.path.join(data_dir, 'bins1')
        bins_1_bins = [os.path.join(data_dir, bins_1_dir, fname)  for fname in ['bin1.fa', 'bin2.fa']]
        bins_1_cids = [[0, 1], [2, 3]]
        
        bins_2_dir = os.path.join(data_dir, 'bins2')
        bins_2_bins = [os.path.join(data_dir, bins_2_dir, fname) for fname in ['bin1.fa', 'bin2.fa', 'bin3.fa']]
        bins_2_cids = [[0], [1,2], [3]]
        
        output_dir = 'outputs'
        refined_bins_sources_file = 'Refined_bins_sources_and_length.txt'
        refined_bins_sources_content = '''Refined_1	80bp	{bins1}__bin1	{bins2}__bin1
Refined_2	80bp	{bins1}__bin1	{bins2}__bin2
Refined_3	80bp	{bins1}__bin2	{bins2}__bin2
Refined_4	80bp	{bins1}__bin2	{bins2}__bin3
'''.format(bins1=bins_1_dir, bins2=bins_2_dir)

        refined_bins_contigs_file = 'Refined_bins_contigs.txt'
        refined_bins_contigs_content = '''Refined_1
seq1
Refined_2
seq2
Refined_3
seq3
Refined_4
seq4
'''
        output_refined_dir = os.path.join(output_dir, "Refined")
        
        os.mkdir(bins_1_dir)
        os.mkdir(bins_2_dir)
        for (bin, cids) in zip(bins_1_bins+bins_2_bins, bins_1_cids+bins_2_cids):
            with open(bin, 'w') as fh:
                fh.write("".join([contigs[i] for i in cids]))
        
        moveback = os.getcwd()
        def cleanup():
            os.chdir(moveback)
            shutil.rmtree(os.path.join(data_dir, bins_1_dir))
            shutil.rmtree(os.path.join(data_dir, bins_2_dir))
            shutil.rmtree(os.path.join(data_dir, output_dir))
            
        try:
            os.chdir(data_dir)
            cmd = "%s -1 %s -2 %s -ms 50" % (path_to_script, bins_1_dir, bins_2_dir)
            subprocess.check_call(cmd, shell=True)
            
            with open(os.path.join(output_dir, refined_bins_sources_file)) as f:
                self.assertEqual(f.read(), refined_bins_sources_content)
            
            with open(os.path.join(output_dir, refined_bins_contigs_file)) as f:
                self.assertEqual(f.read(), refined_bins_contigs_content)
            
            refined = [bin for bin in os.listdir(output_refined_dir) if bin.endswith('.fasta') ]
            self.assertEqual(len(refined), 4)
            
        except:
            cleanup()
            raise
        cleanup()
        
        
        

if __name__ == "__main__":
    unittest.main()

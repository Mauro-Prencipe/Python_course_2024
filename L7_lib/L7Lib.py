import pandas as pd
import numpy as np

class Stat():
          
      def set_size(self):
          self.size=len(self.magnitude)
          return self.size
        
      def average(self):
          ave = 0.
          size = self.set_size()
          self.size=size
          for ix in self.magnitude:
              ave=ave+ix
          ave=ave/size
          self.ave=ave
          self.flag=True
          return ave
        
      def standard_deviation(self, force=True):
          if (not self.flag) or (self.flag and force):
             ave=self.average() 
            
          ave=self.ave
          size=self.size
          std=0.
          for ix in self.magnitude:
              std=std+(ix-ave)**2
                
          std=(std/(size-1))**0.5
          self.std=std
          return std
            
      def describe(self):   
              
          self.average()
          self.standard_deviation()
          self.min_mag=np.min(self.magnitude)
          self.max_mag=np.max(self.magnitude)
          self.depth_min=np.min(self.depth)
          self.depth_max=np.max(self.depth)
                    
          print("data-set: %s" % self.name)
          print("Size: %4i" % self.size)
          print("Minimum magnitude:  %5.2f" % self.min_mag)
          print("Maximum magnitude:  %5.2f" % self.max_mag)
          print("Average magnitude:  %5.2f" % self.ave)
          print("Stand. dev:         %5.2f\n" % self.std)
          print("Depths (km):")
          print("Minimum depth: %6.1f, maximum depth %6.1f\n" %
                (self.depth_min, self.depth_max))
                
class Data(Stat):
    number_of_obj=0  
    obj_files=[]
    obj_names=[]
    flag_array=False
    
    def __init__(self, name):
        self.name=name       
        self.flag=True
        self.size=None
        
    def set_data(self, type_of_data, val):
        
        match type_of_data:
            case 'magnitude':
               self.magnitude=np.array(val)
            
            case 'depth':
               self.depth=np.array(val)
               
            case other:
                print(f"{type_of_data} not implemented")
        
           
    @classmethod
    def read_info(cls, path, info_file):         
        file=path+'/'+info_file
        fi=open(file)
        text=fi.read()
        fi.close()
        text=text.rstrip().splitlines()
        num_lines=len(text)
        cls.number_of_obj=num_lines
             
        for line in text:
            line=line.split()
            cls.obj_files.append(path+'/'+line[0])
            cls.obj_names.append(line[1])
            
    @classmethod
    def setup(cls):
        for obj, file in zip(cls.obj_names, cls.obj_files):
            idata=pd.read_csv(file, sep='|')
            idata.rename(columns={"Depth/Km": "Depth"}, inplace=True)
           
            if not cls.flag_array:
               try:
                  eval(obj).set_data('magnitude', idata.Magnitude)
                  eval(obj).set_data('depth', idata.Depth)
               except NameError:
                  print("Array method should be set as 'region variables'")
                  print("are not defined. Use the command:")
                  print(">>> Data.set_array()")
                  break
            else:
               ipos=cls.obj_dictionary[obj]               
               cls.obj_array[ipos].set_data('magnitude', idata.Magnitude)
               cls.obj_array[ipos].set_data('depth', idata.Depth)
               cls.obj_array[ipos].flag_ready=True           
                    
            
    @classmethod
    def set_array(cls, out=False):  
        cls.flag_array=True
        number_list=list(range(len(cls.obj_names)))
        l_set=list(iset for iset in cls.obj_names)        
        cls.obj_dictionary=dict(zip(cls.obj_names, number_list))
        cls.obj_array=np.array(number_list, dtype='object')
        
        for name in cls.obj_dictionary:
            ipos=cls.obj_dictionary[name]
            cls.obj_array[ipos]=cls(cls.obj_names[ipos])
            
        cls.setup()
        
        if out:
            return cls.obj_dictionary, cls.obj_array 
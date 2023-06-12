import pandas as pd  
import numpy as np
import matplotlib.pyplot as plt

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
          if not self.flag:
             self.average()
             self.standard_deviation()
             self.min_mag=np.min(self.magnitude)
             self.max_mag=np.max(self.magnitude)
                
          print("data-set: %s" % self.name)
          print("Size: %4i" % self.size)
          print("Minimum magnitude:  %5.2f" % self.min_mag)
          print("Maximum magnitude:  %5.2f" % self.max_mag)
          print("Average magnitude:  %5.2f" % self.ave)
          print("Stand. dev:         %5.2f\n" % self.std)
          
          if self.richter_flag:
             inter=self.richter_fit[1]
             slope=self.richter_fit[0]
             print("Richter fit:")
             print("Intercept: %4.2f,   Slope: %6.4f\n\n" % (inter, slope)) 
                  
            
class Data(Stat):
    number_of_sets=0
   
    def __init__(self, name):
                
        self.magnitude=None
        self.name=name
        self.ave=0.
        self.std=0.
        self.flag=False
        self.richter_flag=False
        self.richter_fit=None
        self.nz_log_counts=None
        self.nz_mag=None
        self.min_mag=0
        self.max_mag=0
        
        
    def set_data(self, type_of_data, val):
        if type_of_data == 'magnitude':
           self.magnitude=np.array(val)
    
           
    def richter(self, mgm=0, mgx=0, bins=20): 

        self.describe()
        minimum=self.min_mag
        maximum=self.max_mag
        
        if mgm != 0:
           minimum=mgm
        if mgx != 0:
           maximum=mgx
           
        mag=self.magnitude   
        cases=np.where((mag >= minimum) & (mag <= maximum)) 
        count, mag=np.histogram(mag[cases], bins=bins)          
        nz_counts=np.array([])
        nz_mag=np.array([])
        for ic in range(len(count)):
            if count[ic] != 0:
               nz_counts=np.append(nz_counts, count[ic])
               nz_mag=np.append(nz_mag, mag[ic])                    
        nz_log_counts=np.log10(nz_counts)         
        fit=np.polyfit(nz_mag, nz_log_counts, 1)
        self.richter_fit=fit
        self.nz_log_counts=nz_log_counts
        self.nz_mag=nz_mag
        self.richter_flag=True
        
        print("Fit results:")
        print("Intercept: %4.2f,   Slope: %6.4f" % (fit[1], fit[0]))
                
                
    @classmethod
    def read_info(cls, path, info):
        
        cls.region_names=[]
        cls.region_files=[]
        file=path+'/'+info
        fi=open(file)
        text=fi.read()
        fi.close()
        text=text.rstrip().splitlines()
        num_lines=len(text)
        
        
        for line in text:
            line=line.split()
            cls.region_files.append(line[0])
            cls.region_names.append(line[1])
            
        cls.path=path        
        cls.number_of_sets=num_lines
        
        
    @classmethod
    def setup(cls):
        for region, file in zip(cls.region_names, cls.region_files):
            idata=pd.read_csv(cls.path+'/'+file, sep='|')
            eval(region).set_data('magnitude', idata.Magnitude)
            
    @classmethod
    def describe_all(cls):
        print(f"Number of datasets: {cls.number_of_sets}")
        print(f"Regions: {cls.region_names}\n")
        
        for region in cls.region_names:
            eval(region).describe()


                         
#   ---- User specific functions -------    
    
def richter_plot(region, mgm=0, mgx=0, bins=20):  
    
    region.richter(mgm, mgx, bins)   
    fit=region.richter_fit
    
    mag_min=region.min_mag
    mag_max=region.max_mag
    
    if mgm != 0:
        mag_min=mgm
    if mgx != 0:
        mag_max=mgx
    
    p1x=mag_min
    p2x=mag_max
    region
    p1y=np.polyval(fit, p1x)
    p2y=np.polyval(fit, p2x)
    
    nz_mag=region.nz_mag
    nz_log_counts=region.nz_log_counts
    
    plt.figure()    
    plt.plot((p1x, p2x), (p1y, p2y), "k-", label="Linear regression")
    plt.plot(nz_mag, nz_log_counts, "k*", label="Actual values")
    plt.xlabel('Magnitude')
    plt.ylabel('Log count')
    plt.title('Richter Law')
    plt.legend(frameon=False)
    plt.show()
    
    print("\nParameters of the fit: slope %6.3f, intercept: %6.3f" % (fit[0], fit[1]))
    
    

# ---- starting functions ---- 
       
def start(path='data_files', info_file='L7_tris_info.dat'):
    
    Data.read_info(path, info_file) 
    
if __name__ == "__main__":
    
    start(path='data_files', info_file='L7_tris_info.dat')
    
    for region in Data.region_names:
        exec(region + ' = Data(region)')
                
    Data.setup()    
    
    
   
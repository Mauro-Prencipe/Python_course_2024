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
          
        
            
class Data(Stat):
    number_of_sets=0
    regions=[]
    region_dict={}
   
    def __init__(self, name):
        
        Data.setup(name)
        
        self.magnitude=None
        self.name=name
        self.ave=0.
        self.std=0.
        self.flag=False
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
        
           
    @classmethod       
    def setup(cls,name):
        cls.number_of_sets=cls.number_of_sets+1
        cls.regions.append(name)
        cls.region_dict[name]=cls.number_of_sets-1
        
    @classmethod
    def show(cls):
        print(f"Number of datasets: {cls.number_of_sets}")
        print(f"Regions included: {cls.regions}")
        print(f"Regions dictionary: {cls.region_dict}")
        

path='data_files'
data_files=[]
full_region_files=[]
region_variables=[]

region_files=[
  'earthq_sicilia.dat',
  'earthq_north.dat',
  'earthq_central.dat',
  'earthq_emilia.dat'
]

region_names=[
    'sicilia',
    'north',
    'central',
    'emilia'
]    

   
def setup():
    global Data, region_variables, region_names
    
    
    for region_file in region_files:
        data_file=path+'/'+region_file
        full_region_files.append(data_file)
    
    for region_file in full_region_files:
        idata=pd.read_csv(region_file, sep='|')
        data_files.append(idata)
    
    for region, ir in zip(region_names, range(len(region_names))):
        exec(region + ' = Data(region)')   
        eval(region).set_data('magnitude', data_files[ir].Magnitude)
        region_variables.append(eval(region)) 
    

    
def richter_plot(region, mgm=0, mgx=0, bins=20):  
    
    ipos=Data.region_dict[region]
    ireg=region_variables[ipos]
    ireg.richter(mgm, mgx, bins)   
    fit=ireg.richter_fit
    
    mag_min=ireg.min_mag
    mag_max=ireg.max_mag
    
    if mgm != 0:
        mag_min=mgm
    if mgx != 0:
        mag_max=mgx
    
    p1x=mag_min
    p2x=mag_max
    region
    p1y=np.polyval(fit, p1x)
    p2y=np.polyval(fit, p2x)
    
    nz_mag=ireg.nz_mag
    nz_log_counts=ireg.nz_log_counts
    
    plt.figure()    
    plt.plot((p1x, p2x), (p1y, p2y), "k-", label="Linear regression")
    plt.plot(nz_mag, nz_log_counts, "k*", label="Actual values")
    plt.xlabel('Magnitude')
    plt.ylabel('Log count')
    plt.title('Richter Law')
    plt.legend(frameon=False)
    plt.show()
    
    print("\nParameters of the fit: slope %6.3f, intercept: %6.3f" % (fit[0], fit[1]))
    
# Interfaces for the describe method of the Stat class
def describe(region):
    ipos=Data.region_dict[region]
    region_variables[ipos].describe()
    
def describe_all():
    for name in region_names:
        ipos=Data.region_dict[name]
        region_variables[ipos].describe()
      
    
if __name__ == "__main__":
    setup()
    Data.show()
    print("")
    describe_all()
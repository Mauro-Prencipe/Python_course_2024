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
          
          if self.richter_flag:
             inter=self.richter_fit[1]
             slope=self.richter_fit[0]
             print("Richter fit:")
             print("Intercept: %4.2f,   Slope: %6.4f\n" % (inter, slope))
                  
            
class Data(Stat):
    number_of_sets=0    
    
    def __init__(self, name):
                
        self.magnitude=None
        self.depth=None
        self.name=name
        self.ave=0.
        self.std=0.
        self.flag=False
        self.richter_flag=False
        self.richter_fit=None
        self.nz_log_counts=None
        self.nz_mag=None
        self.__bins=20
        
        
    def set_data(self, type_of_data, val):
        
        """
        Loads magnitudes and depths of quake events as attributes
        of instances of the Data class
    
        Input:
            type_of_data: can take the values 'magnitude' or 'depth'
            val: array of corresponding numerical values
        """
        
        match type_of_data:
            case 'magnitude':
               self.magnitude=np.array(val)
            case 'depth':
               self.depth=np.array(val)
            case other:
                print(f"{type_of_data} not implemented")
                
    @property
    def bins(self):
        return self.__bins
    
    @bins.setter
    def bins(self, bins_value):
        self.__bins=bins_value
                         
           
    def richter(self, mgm=0, mgx=0, d_min=0, d_max=0): 
 
        """
        Computes Richter's law fit
        
        Input:
             mgm: if not 0, minimun magnitude (default 0)
             mgx: if not 0, maximum magnitude (default 0)
             d_min: if not 0, minimum depth (default 0)
             d_max: if not 0, maximim depth (default 0)
        """
        self.richter_flag=False
        self.describe()
        
        minimum=np.min(self.magnitude)
        maximum=np.max(self.magnitude)     
        minimum_d=np.min(self.depth)
        maximum_d=np.max(self.depth)
        
        if mgm != 0:
           minimum=mgm
        if mgx != 0:
           maximum=mgx           
        if d_min != 0:
           minimum_d=d_min
        if d_max != 0:
           maximum_d=d_max 
        
        mag=self.magnitude 
        depth=self.depth
        
        cases_mag=np.where((mag >= minimum) & (mag <= maximum))
        cases_depth=np.where((depth >= minimum_d) & (depth <= maximum_d))
        cases=np.intersect1d(cases_mag, cases_depth)
        
        count, mag=np.histogram(mag[cases], bins=self.bins)          
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
        print(f"Number of events: {len(cases)}")
        print("Intercept: %4.2f,   Slope: %6.4f" % (fit[1], fit[0]))
                        
                
    @classmethod
    def read_info(cls, path, info):
        """
        Reads an information file containing names of data files and
        names of regions, for the creation of the quakes dataset.
        
        Input:
            path: location of the info file
            info: name of the info file
        """
        
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
            idata.rename(columns={"Depth/Km": "Depth"}, inplace=True)
            eval(region).set_data('magnitude', idata.Magnitude)
            eval(region).set_data('depth', idata.Depth)
            
    @classmethod
    def describe_all(cls):
        print(f"Number of datasets: {cls.number_of_sets}")
        print(f"Regions: {cls.region_names}\n")
        
        for region in cls.region_names:
            eval(region).describe()
            print("-"*35)
            
    @classmethod
    def richter_all(cls, mgm=0, mgx=0, d_min=0, d_max=0):
        for region in cls.region_names:
            eval(region).richter(mgm, mgx, d_min, d_max)
            print("")
            print("-"*35)

                         
#   ---- User specific functions -------    
    
def richter_plot(region, mgm=0, mgx=0, d_min=0, d_max=0, bins=20):  
    
    region.bins=bins
    region.richter(mgm, mgx, d_min, d_max)   
    fit=region.richter_fit
    
    mag_min=region.min_mag
    mag_max=region.max_mag
    
    if mgm != 0:
        mag_min=mgm
    if mgx != 0:
        mag_max=mgx
           
    p1x=mag_min
    p2x=mag_max    
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
    
    
def depth_distribution(region, bins=30):
    depth=region.depth

    plt.figure()
    plt.hist(depth, bins)
    plt.xlabel("Depth (km)")
    plt.ylabel("Number")
    plt.title(f"Region: {region.name}")
    plt.show()
   
    

# ---- starting functions ---- 
       
def start(path='data_files', info_file='L7_tris_info.dat'):    
    Data.read_info(path, info_file) 
    
if __name__ == "__main__":
    
    start()
    
    for region in Data.region_names:
        exec(region + ' = Data(region)')
                
    Data.setup()    
    
    
   
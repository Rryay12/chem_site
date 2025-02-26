import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

class reaction:
    
    def __init__(self):
        self.molecule_info = {}
        self.k = 1
        plt.switch_backend('Agg') 
        
    def add_molecule(self,name:str,degree:int,initial_concentration:float,is_product:bool,equilibrium_concentration:float = 0.0):
        self.molecule_info[name] = {"degree": degree if is_product else -degree,
                                    "initial_concentration":initial_concentration,
                                    "is_product":is_product,
                                    "equilibrium_concentration":equilibrium_concentration}
        
    
    def calc_k(self) -> None:
        
        current_conc = self.get_eq_conc_list()
        degree_list = self.get_degree_list()
        
        return np.prod([(current_conc[i] + 0.001)**degree_list[i] for i in range(len(current_conc))])
    
    def set_k(self,k:int) -> None:
        self.k = k
        
    def get_degree_list(self):
        return [self.molecule_info[key]["degree"] for key in self.molecule_info.keys()]

    def get_init_conc_list(self):
        return [self.molecule_info[key]["initial_concentration"] for key in self.molecule_info.keys()]

    def get_eq_conc_list(self):
        return [self.molecule_info[key]["equilibrium_concentration"] for key in self.molecule_info.keys()]

    def reaction(self, t,current_conc):
        return_list = []
        degree_list = self.get_degree_list()
        
        epsilon = 1e-10
        rate = self.k * np.prod([(current_conc[i] + epsilon) ** degree_list[i] for i in range(len(current_conc))])
        
        for i in range(len(current_conc)):
            return_list.append(degree_list[i] * rate)
        
        return return_list
    
    def simulate(self,t_span,num_points):
        t_eval = np.linspace(t_span[0], t_span[1], num_points)
        
        sol = solve_ivp(self.reaction, t_span, self.get_init_conc_list(), t_eval=t_eval, method='LSODA')
        return sol.t, sol.y
    
    def make_graph(self,t_span = None,num_points=100,link = ""):
        if t_span==None:
            t_span = (0,int(10/self.k))
        
        
        t,y = self.simulate(t_span,num_points)
        
        
        plt.figure(figsize=(8,5))
        
        for no,molecule in enumerate(self.molecule_info.keys()):
            plt.plot(t, y[no], label=molecule)
            
        plt.xlabel('Time (s)')
        plt.ylabel('Concentration (M)')
        plt.title('Multi-Species Reaction Simulation')
        plt.legend()
        plt.grid()
        
        plt.savefig(link+"/reaction")
        
    def reset(self):
        self.molecule_info = {}
        self.k = 1
        
    


        
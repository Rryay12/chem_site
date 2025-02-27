import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

class reaction:
    
    def __init__(self):
        self.molecule_info = {}
        self.k = 1
        self.K_eq = 1
        plt.switch_backend('Agg') 
        
    def add_molecule(self,name:str,degree:int,initial_concentration:float,is_product:bool,eq_conc:float = 1):
        self.molecule_info[name] = {"degree": degree if is_product else -degree,
                                    "initial_concentration":initial_concentration,
                                    "is_product":is_product,
                                    "eq_conc":eq_conc}
        
    def set_k_eq(self):
        epsilon = 1e-10 
        eq_conc = self.get_init_conc_list()
        self.K_eq = np.prod([(eq_conc[i] + epsilon) ** eq_conc[i] for i in range(len(eq_conc))])
        
    def set_k(self,k:int) -> None:
        self.k = k
        
    def get_degree_list(self):
        return [self.molecule_info[key]["degree"] for key in self.molecule_info.keys()]

    def get_eq_conc_list(self):
        return [self.molecule_info[key]["eq_conc"] for key in self.molecule_info.keys()]

    def get_init_conc_list(self):
        return [self.molecule_info[key]["initial_concentration"] for key in self.molecule_info.keys()]

    def reaction(self, t, current_conc):
        self.set_k_eq()
        return_list = []
        degree_list = self.get_degree_list()
        epsilon = 1e-10  
        
        forward_rate = self.k * np.prod([(current_conc[i] + epsilon) ** abs(degree_list[i]) 
                                        for i in range(len(current_conc)) if degree_list[i] < 0])
        
        reverse_rate = (self.k / self.K_eq) * np.prod([(current_conc[i] + epsilon) ** abs(degree_list[i]) 
                                                for i in range(len(current_conc)) if degree_list[i] > 0])
        
        net_rate = forward_rate - reverse_rate
        
        for i in range(len(current_conc)):
            return_list.append(degree_list[i] * net_rate)
            
        return return_list


    
    def simulate(self,t_span,num_points):
        t_eval = np.linspace(t_span[0], t_span[1], num_points)
        
        sol = solve_ivp(self.reaction, t_span, self.get_init_conc_list(), t_eval=t_eval, method='BDF')
        return sol.t, sol.y
    
    def make_graph(self,t_span = None,num_points=100,link = ""):
        if t_span==None:
            t_span = (0,10/self.k)
        
        
        t,y = self.simulate(t_span,num_points)
        
        
        plt.figure(figsize=(8,5))
        
        for no,molecule in enumerate(self.molecule_info.keys()):
            plt.plot(t, y[no], label=molecule)
            
        plt.xlabel('Time (s)')
        plt.ylabel('Concentration (M)')
        plt.title('Multi-Species Reaction Simulation')
        plt.legend()
        plt.grid()
        
        plt.savefig(link+"reaction")
        
    def reset(self):
        self.molecule_info = {}
        self.k = 1
        
    


        
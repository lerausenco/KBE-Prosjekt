from duralok import Duralok


f = open("C:\\Users\\lera_\\OneDrive\\Dokumenter\\NTNU\\KBE\\KBE-Prosjekt\\Nodes\\params.txt", "r")
text = f.read()
text = text.replace("'","")
text = text.replace(" ", "")
text = text.replace("{","")
text = text.replace("}", "")

param_pairs = text.split(",")

param_dict = {}

for param_pair in param_pairs:
    param_name = param_pair.split(":")[0]
    param_val = param_pair.split(":")[1]

    param_dict[param_name] = param_val

pipe_diam = float(param_dict['pipe_diam'])
lock_th = float(param_dict['wall_th'])
material = param_dict['material_pref']
material = material.replace(" ", "")

#MAXIMUM SIMULATION
name = "node"+param_dict["name"][:10] + "_max"
myduralok = Duralok(
    material, name, pipe_diam, lock_th)
myduralok.save_part()
myduralok.make_fem_model()

myduralok.do_sim(
    NFORCE=float(param_dict['N_max']),
    VFORCE=float(param_dict['V_max']),
    MOMENT=float(param_dict['M_max']))
myduralok.make_gif()
myduralok.close_file()


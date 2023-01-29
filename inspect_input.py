from plyfile import PlyData

INPUT = input("Please fill in thresholds for checking intensity, separated by commas. Example: 1,2,3,4.\nTo use option DefaultValues1 (1-10), enter 1.\nTo use option DefaultValues2 (1-30), enter 2.\nThresholds: ")
print("Running...Please wait")
if INPUT =="1":
    THRESHOLDS = range(1,11)
elif INPUT == "2":
    THRESHOLDS = range(1,31)
else:
    THRESHOLDS = [int(i) for i in INPUT.split(",")]

STATS = dict(zip(THRESHOLDS, [0 for _ in range(len(THRESHOLDS))]))
FILE_NAME = "mesh.ply"

with open(FILE_NAME,'rb') as f:
    plydata = PlyData.read(f)  


# A point has format (x_coor, y_coor, z_coor, intensity)
for point in plydata.elements[0].data:
    intensity = point[3]
    for check in THRESHOLDS:
        if intensity <= check:
            STATS[check] += 1

print()
for threshold, value in STATS.items():
    print("Percent of points in dataset with intensity <=",threshold,"is:",value/len(plydata.elements[0].data),"%")












# cube_list = plydata.elements[0].data
# cube_list = cube_list[:num_init_points]

# FILTERING DENSITY:
# cube_list = [i for i in plydata.elements[0].data if i[3] >= 2]

# print("Num points are: ",len(cube_list))
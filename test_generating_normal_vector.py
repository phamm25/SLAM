#   SCHEMA FOR PLYDATA ELEMENTS:
"""
(PlyElement('vertex', (PlyProperty('x', 'float'), PlyProperty('y', 'float'), PlyProperty('z', 'float'), PlyProperty('intensity', 'float')), count=4669049, comments=[]),    -> element 0
PlyElement('camera', (PlyProperty('view_px', 'float'), PlyProperty('view_py', 'float'), PlyProperty('view_pz', 'float'),                                                    -> element 1
                    PlyProperty('x_axisx', 'float'), PlyProperty('x_axisy', 'float'), PlyProperty('x_axisz', 'float'), 
                    PlyProperty('y_axisx', 'float'), PlyProperty('y_axisy', 'float'), PlyProperty('y_axisz', 'float'), 
                    PlyProperty('z_axisx', 'float'), PlyProperty('z_axisy', 'float'), PlyProperty('z_axisz', 'float'), 
                    PlyProperty('focal', 'float'), PlyProperty('scalex', 'float'), PlyProperty('scaley', 'float'), 
                    PlyProperty('centerx', 'float'), PlyProperty('centery', 'float'), 
                    PlyProperty('viewportx', 'int'), PlyProperty('viewporty', 'int'), 
                    PlyProperty('k1', 'float'), PlyProperty('k2', 'float')), count=1, comments=[]))
"""


import open3d as o3d
import numpy as np
from plyfile import PlyData

# # print("Load a ply point cloud, print it, and render it")
# # ply_point_cloud = o3d.data.PLYPointCloud()
# # pcd = o3d.io.read_point_cloud(ply_point_cloud.path)
# # print(np.asarray(pcd.normals)[:3])
# # print(np.asarray(pcd.points)[:3])

# # print(np.asarray(pcd.normals).shape)
# # print(np.asarray(pcd.points).shape)

# # o3d.visualization.draw_geometries([pcd],
# #                                   zoom=0.3412,
# #                                   front=[0.4257, -0.2125, -0.8795],
# #                                   lookat=[2.6172, 2.0475, 1.532],
# #                                   up=[-0.0694, -0.9768, 0.2024])


# # original = o3d.io.read_point_cloud("mesh.ply")

# with open('mesh.ply','rb') as f:
#     plydata = PlyData.read(f)
# cube_list = plydata.elements[0].data
# camera = plydata.elements[1].data

# print(cube_list)
# print(camera)
# # print(plydata.elements)

# # for i in range(10):
# #     print(i,cube_list[i], camera[i])


"""
Testing estimate_normals, normalize_normal,voxel_down_sample and remove_radius_outlier
"""
pcd = o3d.io.read_point_cloud("mesh.ply")
# pcd = pcd.voxel_down_sample(voxel_size=0.5)

# # nb_points = num points in radius/ radius = radius of sphere/ return: Tuple[open3d.geometry.PointCloud, List[int]]
# pcd = pcd.remove_radius_outlier(nb_points=5, radius=0.5)[0]

pcd.estimate_normals(fast_normal_computation=False)
# pcd.normalize_normals()
pcd.paint_uniform_color([0, 0.5, 0.7])


o3d.visualization.draw_geometries(
    [pcd],
    zoom=0.3412,
    front=[0.4257, -0.2125, -0.8795],
    lookat=[2.6172, 2.0475, 1.532],
    up=[-0.0694, -0.9768, 0.2024],
)

"""
Test filtering and down sampling data for better Marching Cubes Input
"""
# pcd = o3d.io.read_point_cloud("mesh.ply")
# pcd = pcd.voxel_down_sample(voxel_size=1.2)

# print(np.asarray(pcd.points)[:10])
# # nb_points = num points in radius/ radius = radius of sphere/ return: Tuple[open3d.geometry.PointCloud, List[int]]
# # pcd = pcd.remove_radius_outlier(nb_points=5, radius=1.5)[0]

# # pcd.paint_uniform_color([0, 0.5, 0.7])
# o3d.visualization.draw_geometries(
#     [pcd],
#     zoom=0.3412,
#     front=[0.4257, -0.2125, -0.8795],
#     lookat=[2.6172, 2.0475, 1.532],
#     up=[-0.0694, -0.9768, 0.2024],
# )
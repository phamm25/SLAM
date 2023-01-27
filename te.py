# # import open3d as o3d

# # bunny = o3d.data.BunnyMesh()
# # mesh = o3d.io.read_triangle_mesh(bunny.path)
# # mesh.compute_vertex_normals()

# # pcl = mesh.sample_points_poisson_disk(number_of_points=2000)
# # hull, _ = pcl.compute_convex_hull()
# # hull_ls = o3d.geometry.LineSet.create_from_triangle_mesh(hull)
# # hull_ls.paint_uniform_color((1, 0, 0))
# # o3d.visualization.draw_geometries([pcl, hull_ls])


# from plyfile import PlyData, PlyElement
# import math
# import json
# from MarchingCubesVer2 import create_cube_from_midpoint
# import open3d
# import numpy as np


# SIDE = 100
# HALF_SIDE = SIDE / 2


# OFFSET_GRID = {}

# LIST_OF_TRI = []


# with open("permutations.txt") as json_file:
#     PERMUTATIONS = json.load(json_file)

# MAPPING = {
#     "p1": (-1 * HALF_SIDE, -1 * HALF_SIDE, 1 * HALF_SIDE),
#     "p2": (-1 * HALF_SIDE, 1 * HALF_SIDE, 1 * HALF_SIDE),
#     "p3": (1 * HALF_SIDE, 1 * HALF_SIDE, 1 * HALF_SIDE),
#     "p4": (1 * HALF_SIDE, -1 * HALF_SIDE, 1 * HALF_SIDE),
#     "p5": (-1 * HALF_SIDE, -1 * HALF_SIDE, -1 * HALF_SIDE),
#     "p6": (-1 * HALF_SIDE, 1 * HALF_SIDE, -1 * HALF_SIDE),
#     "p7": (1 * HALF_SIDE, 1 * HALF_SIDE, -1 * HALF_SIDE),
#     "p8": (1 * HALF_SIDE, -1 * HALF_SIDE, -1 * HALF_SIDE),
# }

# REVERSE_MAPPING = {
#     (-HALF_SIDE, -HALF_SIDE, HALF_SIDE): "p1",
#     (-HALF_SIDE, HALF_SIDE, HALF_SIDE): "p2",
#     (HALF_SIDE, HALF_SIDE, HALF_SIDE): "p3",
#     (HALF_SIDE, -HALF_SIDE, HALF_SIDE): "p4",
#     (-HALF_SIDE, -HALF_SIDE, -HALF_SIDE): "p5",
#     (-HALF_SIDE, HALF_SIDE, -HALF_SIDE): "p6",
#     (HALF_SIDE, HALF_SIDE, -HALF_SIDE): "p7",
#     (HALF_SIDE, -HALF_SIDE, -HALF_SIDE): "p8",
# }

# NUM_INIT_POINTS = 100


# with open("mesh.ply", "rb") as f:
#     plydata = PlyData.read(f)

# cube_list = plydata.elements[0].data
# cube_list = cube_list[:NUM_INIT_POINTS]
# VOXEL_DATA = list(
#     set(
#         [
#             (
#                 SIDE * math.floor(p[0]) + HALF_SIDE,
#                 SIDE * math.floor(p[1]) + HALF_SIDE,
#                 SIDE * math.floor(p[2]) + HALF_SIDE,
#             )
#             for p in cube_list
#         ]
#     )
# )
# print(cube_list)
# print()
# print(VOXEL_DATA)

# for mid in VOXEL_DATA:
#     # print("orig cube is: ",orig_cub)
#     for off_cube in create_cube_from_midpoint(mid):
#         # print("off_cub is: ",off_cube)
#         if OFFSET_GRID.get(off_cube) == None:
#             OFFSET_GRID[off_cube] = set([mid])
#         else:
#             OFFSET_GRID[off_cube].add(mid)
# # print("Number of offset_grid: ",len(OFFSET_GRID))

# print()
# # print(OFFSET_GRID)

# for mid, p_inside in OFFSET_GRID.items():
#     for p in p_inside:
#         print(p[0], p[1], p[2])
#         print(mid[0], mid[1], mid[2])
#         print((p[0] - mid[0], p[1] - mid[1], p[2] - mid[2]))
#         print('\n')
#     lookup = "_".join(
#         sorted(
#             [
#                 REVERSE_MAPPING[(p[0] - mid[0], p[1] - mid[1], p[2] - mid[2])]
#                 for p in p_inside
#             ]
#         )
#     )
#     # print(mid, p_inside, lookup)
#     triangles = PERMUTATIONS[lookup]
#     for tri in triangles:
#         temp_tri = []
#         for point in tri:
#             temp_p = (mid[0] + point[0], mid[1] + point[1], mid[2] + point[2])
#             temp_tri.append(temp_p)
#         LIST_OF_TRI.append((temp_tri[0], temp_tri[1], temp_tri[2]))


# # march_cube.main(NUM_INIT_POINTS)
# # march_cube.main()

# mesh = open3d.geometry.TriangleMesh()
# np_vertices = np.array([[None for i in range(3)] for j in range(len(LIST_OF_TRI) * 3)])


# for i in range(len(LIST_OF_TRI)):
#     for j in range(3):
#         for k in range(3):
#             np_vertices[3 * i + j][k] = LIST_OF_TRI[i][j][k]

# np_triangles = np.array(
#     [[j * 3 + i for i in range(3)] for j in range(len(np_vertices) // 3)]
# ).astype(np.int32)
# mesh.vertices = open3d.utility.Vector3dVector(np_vertices)

# mesh.triangles = open3d.utility.Vector3iVector(np_triangles)


# print("almost done")


# # print(type(mesh))
# # print(len(march_cube.LIST_OF_TRI))
# # print(np.asarray(mesh.vertices))
# # print(len(np.asarray(mesh.vertices)))
# # print(np.asarray(mesh.triangles))
# # print(len(np.asarray(mesh.triangles)))

# open3d.io.write_triangle_mesh("MarchingCubesOutput.ply", mesh, compressed=True)
# # open3d.io.write_triangle_mesh('test_mesh.ply', mesh, write_ascii = True)


# print("DONE!")
# # open3d.visualization.draw_geometries([mesh])

def floor(value, floor_base):
    a = value // floor_base
    a = a*floor_base
    return a

print(floor(0.44999999999998863,0.9))
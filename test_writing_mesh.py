import open3d 
import numpy as np
import MarchingCubesVer2 as march_cube

NUM_INIT_POINTS = 1000


# march_cube.main(NUM_INIT_POINTS)
march_cube.main()

mesh = open3d.geometry.TriangleMesh()
np_vertices = np.array([[None for i in range(3)] for j in range(len(march_cube.LIST_OF_TRI)*3)])


for i in range(len(march_cube.LIST_OF_TRI)):
    for j in range(3):
        for k in range(3):
            np_vertices[3*i+j][k] = march_cube.LIST_OF_TRI[i][j][k]

np_triangles = np.array([[j*3+i for i in range(3)] for j in range(len(np_vertices)//3)]).astype(np.int32)
mesh.vertices = open3d.utility.Vector3dVector(np_vertices)

mesh.triangles = open3d.utility.Vector3iVector(np_triangles)
mesh.paint_uniform_color([1, 0.706, 0])





# print(type(mesh))
# print(len(march_cube.LIST_OF_TRI))
# print(np.asarray(mesh.vertices))
# print(len(np.asarray(mesh.vertices)))
# print(np.asarray(mesh.triangles))
# print(len(np.asarray(mesh.triangles)))

open3d.io.write_triangle_mesh('MarchingCubesOutput.ply', mesh, compressed=True)
# open3d.io.write_triangle_mesh('test_mesh.ply', mesh, write_ascii = True)


print('DONE!')
# open3d.visualization.draw_geometries([mesh])









# import open3d as o3d
# import numpy as np
# import copy

# if __name__ == "__main__":
#     bunny = o3d.data.BunnyMesh()
#     mesh = o3d.io.read_triangle_mesh(bunny.path)
#     mesh.compute_vertex_normals()

#     mesh = mesh.subdivide_midpoint(number_of_iterations=2)
#     vert = np.asarray(mesh.vertices)
#     min_vert, max_vert = vert.min(axis=0), vert.max(axis=0)
#     for _ in range(30):
#         cube = o3d.geometry.TriangleMesh.create_box()
#         cube.scale(0.005, center=cube.get_center())
#         cube.translate(
#             (
#                 np.random.uniform(min_vert[0], max_vert[0]),
#                 np.random.uniform(min_vert[1], max_vert[1]),
#                 np.random.uniform(min_vert[2], max_vert[2]),
#             ),
#             relative=False,
#         )
#         mesh += cube
#     mesh.compute_vertex_normals()
#     print("Displaying input mesh ...")
#     o3d.visualization.draw([mesh])

#     print("Clustering connected triangles ...")
#     with o3d.utility.VerbosityContextManager(
#             o3d.utility.VerbosityLevel.Debug) as cm:
#         triangle_clusters, cluster_n_triangles, cluster_area = (
#             mesh.cluster_connected_triangles())
#     triangle_clusters = np.asarray(triangle_clusters)
#     cluster_n_triangles = np.asarray(cluster_n_triangles)
#     cluster_area = np.asarray(cluster_area)

#     print("Displaying mesh with small clusters removed ...")
#     mesh_0 = copy.deepcopy(mesh)
#     triangles_to_remove = cluster_n_triangles[triangle_clusters] < 100
#     mesh_0.remove_triangles_by_mask(triangles_to_remove)
#     o3d.visualization.draw([mesh_0])



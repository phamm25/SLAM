import open3d as o3d

print("Testing mesh in Open3D...")
# armadillo_mesh = o3d.data.ArmadilloMesh()
try:

    mesh = o3d.io.read_triangle_mesh('MarchingCubesOutput.ply')
    mesh.paint_uniform_color([0, 0.5, 0.7])
    # mesh = o3d.io.read_triangle_mesh('TestNormalVector.ply')


    # mesh.compute_vertex_normals()
    print('DONE!')
    o3d.visualization.draw_geometries([mesh])

    # mesh = o3d.io.read_triangle_mesh('MarchingCubesOutput.ply')
    # mesh_in = mesh.filter_smooth_simple(number_of_iterations=1)
    # mesh_in.compute_vertex_normals()
    # print('DONE!')
    # o3d.visualization.draw_geometries([mesh_in])


except:
    print('error!')
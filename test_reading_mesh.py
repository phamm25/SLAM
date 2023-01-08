import open3d as o3d

print("Testing mesh in Open3D...")
# armadillo_mesh = o3d.data.ArmadilloMesh()
try:
    mesh = o3d.io.read_triangle_mesh('test_mesh.ply')
    mesh.compute_vertex_normals()
    print('DONE!')
    o3d.visualization.draw_geometries([mesh])
except:
    print('error!')
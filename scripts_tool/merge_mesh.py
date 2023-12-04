import click
from os.path import join
import torch
import loc_ndf.models.models as models
import open3d as o3d
import os
import copy

@click.command()
# Add your options here
@click.option('--checkpoint',
              '-c',
              type=str,
              help='path to the ckpt file (.ckpt)',
              required=True)

# @click.argument('checkpoint',
#                 nargs=-1,
#                 required=True)

class merge_Visualizer():
    def __init__(self, checkpoint, width=1920, height=1080):
        self.device = 'cuda'

        self.vis = o3d.visualization.VisualizerWithKeyCallback()

        print(f"checkpoint(path) : {checkpoint}")

        checkpoints = [os.path.join(checkpoint, file) for file in os.listdir(checkpoint) if file.endswith('.ckpt') and 'best-v' in file]

        print(f"checkpoints(.ckpt) : {checkpoints}, len(checkpoints) : {len(checkpoints)}")

        
        self.models = [models.LocNDF.load_from_checkpoint(
        ckpt, hparams=torch.load(ckpt)['hyper_parameters']).to(device=self.device) for ckpt in checkpoints]

        print(f"len(self.models) : {len(self.models)}")

        self.rel_pose = None
        self.poses = []
        # for i in range(len(self.models)-1):
        print(f"len(self.models) : {len(self.models)}")

        for model in self.models:
            # print(f"model : {model}")
            pose = torch.tensor(
                model.hparams['data']['pose'], device=self.device, dtype=torch.double).reshape(4, 4)
            
            if self.rel_pose is None:
                self.rel_pose = torch.linalg.inv(pose)
           
            self.poses.append((self.rel_pose @ pose).to(device=self.device))

        print(f"len(self.poses) : {len(self.poses)}")

        num_voxels = 400
        self.nv = [num_voxels, num_voxels, num_voxels//10]
        self.threshold = 0.01

        self.run()

    def run(self):
        print(f"In def run(self):")

        coords = []
        coord = o3d.geometry.TriangleMesh.create_coordinate_frame()
        
        coords.append(coord)

        for pose in self.poses:
            coord_cp = copy.deepcopy(coord).transform(pose.cpu().numpy())
            coord_cp.scale(7.0, center=coord_cp.get_center())
            coords.append(coord_cp)

        meshes = []
        i = 0
        for model in self.models:
            mesh = model.get_mesh(self.nv, self.threshold, mask=model.get_occupancy_mask(
        self.nv).cpu().numpy())  # ,file=file)
            mesh.transform(self.poses[i].cpu().numpy())
            meshes.append(mesh)
            i += 1

        # Visualization
        o3d.visualization.draw_geometries(coords + meshes)


if __name__ == "__main__":
    vis = merge_Visualizer()
    # vis.run()
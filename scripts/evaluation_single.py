import argparse
from src.utils import load_video
from src.ssim import compute_ssim
from src.psnr import compute_psnr
from src.clip import compute_clip_score_single
from src.fwe import compute_fwe
from src.of_consistency import compute_video_optical_flow, compute_optical_flow_consistency
from omegaconf import OmegaConf

def evaluation_single(
    real_video_path: str,
    generated_video_path: str,
    prompt: str,
    width: int,
    height: int,
    frames_per_video: int
):
    frame_size = (width, height)

    # Load videos
    print(f"\n[INFO] Loading real video from {real_video_path}...")
    real_video = load_video(real_video_path, frames_per_video, frame_size)
    if real_video is None:
        print("[ERROR] Loading real video was not successful.")

    print(f"\n[INFO] Loading generated video from {generated_video_path}...")
    generated_video = load_video(generated_video_path, frames_per_video, frame_size)
    if generated_video is None:
        print("[ERROR] Loading generated video was not successful.")


    # Compute Average SSIM Score:
    print("\n[INFO] Computing SSIM Score [1/5]...")
    ssim_score = compute_ssim(generated_video, real_video, frame_size)


    # Compute PSNR:
    print("\n[INFO] Computing PSNR [2/5]...")
    psnr = compute_psnr(generated_video, real_video)


    # Compute CLIP score
    print("\n[INFO] Computing CLIP Score [3/5]...")
    clip_score = compute_clip_score_single(generated_video, prompt, frame_size)


    # Compute Flow Warping Error
    print("\n[INFO] Computing Flow Warping Error [4/5]...")
    fwe = compute_fwe(generated_video, real_video, frame_size)


    # Compute Optical Flow Consistency
    print("\n[INFO] Computing Optical Flow Consistency [5/5]...")
    generated_flows = compute_video_optical_flow(generated_video)
    reference_flows = compute_video_optical_flow(real_video)
    consistency_metric = compute_optical_flow_consistency(generated_flows, reference_flows)


    # Metrics recap
    print("\n******************* METRICS RESULTS ************************\n")
    print(f'[RES] CLIP Score: {round(clip_score.item(), 5)}')
    print(f'[RES] SSIM: {round(ssim_score, 5)}')
    print(f'[RES] PSNR: {round(psnr.item(), 5)} dB')
    print(f'[RES] Flow Warping Error: {round(fwe, 5)}')
    print(f'[RES] Optical Flow Consistency: {round(consistency_metric, 5)}')
    print("**************************************************************")

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="./configs/evaluation_single.yaml")
    args = parser.parse_args()
    
    evaluation_single(**OmegaConf.load(args.config))
# USM Sample from Digimon Story: Cyber Sleuth (PC)
# Uses same key for both HCA and USM decryption
USM_KEY = 2897314143465725881
from . import sample_file_path, temp_file_path
from PyCriCodecsEx.usm import USM, USMBuilder, ADXCodec, HCACodec, VP9Codec
import ffmpeg, os
def mux_av(video_src: str, audio_src: str, output: str, delete: bool = False):
    (        
        ffmpeg.output(
            ffmpeg.input(video_src), 
            ffmpeg.input(audio_src),
            output, 
            vcodec='copy',
            acodec='copy',
        ).overwrite_output()
    ).run()
    if delete:
        print('* Cleaning up temporary files')        
        os.unlink(video_src)
        os.unlink(audio_src)
    print(f'* Result available at: {output}')
def decode_one(path : str):
    usm = USM(path, USM_KEY)
    audio = usm.get_audios()
    video = usm.get_video()
    audio = audio[0] if audio else None
    return audio, video
def test_usm_decode_and_mux():    
    saved_video = temp_file_path('tmp_video.ivf') # <- must be IVF container
    saved_audio = temp_file_path('tmp_audio.wav')    
    result = temp_file_path('muxed_result1.mp4')    
    # Decode    
    audio, video = decode_one(temp_file_path('S01_B.usm'))
    video.save(saved_video)
    audio.save(saved_audio)
    # Mux
    mux_av(saved_video, saved_audio, result)
    print('Remux Done.')
    # Rebuild
    usm_builder = USMBuilder(USM_KEY)
    usm_builder.add_video(saved_video)
    usm_builder.add_audio(HCACodec(saved_audio, key=USM_KEY))
    rebuilt_usm_path = temp_file_path('rebuilt_usm.usm')
    usm_builder.save(rebuilt_usm_path)
    print(f'Rebuilt USM saved at: {rebuilt_usm_path}')
    # Decoded again
    audio2, video2 = decode_one(rebuilt_usm_path)
    saved_video2 = temp_file_path('tmp_video2.ivf') # <- must be IVF container
    saved_audio2 = temp_file_path('tmp_audio2.wav')    
    result2 = temp_file_path('muxed_result2.mp4')    
    video2.save(saved_video2)
    audio2.save(saved_audio2)
    # Mux again
    mux_av(saved_video2, saved_audio2, result2)
    print('Remux Done (decode-mux).')

if __name__ == "__main__":
    test_usm_decode_and_mux()
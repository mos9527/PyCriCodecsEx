# USM Sample from Digimon Story: Cyber Sleuth (PC)
# Uses same key for both HCA and USM decryption
# HCA Key {2897314143465725881}, // 283553DCE3FD5FB9
# USM Key 2897314143465725881
from . import sample_file_path, temp_file_path
from PyCriCodecsEx.usm import USM, USMBuilder, ADXCodec, HCACodec

def test_usm_decode_and_mux():
    usm = USM(temp_file_path('S01_B.usm'), 2897314143465725881)
    audio = usm.get_audios()
    video = usm.get_video()
    audio = audio[0] if audio else None
    # Mux into MP4
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
    saved_video = temp_file_path('tmp_video.mp4')
    saved_audio = temp_file_path('tmp_audio.wav')
    saved_hca = temp_file_path('tmp_audio.hca')
    result = temp_file_path('muxed_result1.mp4')
    open(saved_hca,'wb').write(audio.get_hca())
    video.save(saved_video)
    audio.save(saved_audio)
    mux_av(saved_video, saved_audio, result)
    print('Remux Done.')

if __name__ == "__main__":
    test_usm_decode_and_mux()
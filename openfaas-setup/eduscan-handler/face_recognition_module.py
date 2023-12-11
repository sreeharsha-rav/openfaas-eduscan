import os
import json
from processVideo_module import process_video
from helper_functions import download_video_file, get_academic_info, write_results, upload_file

def face_recognition_handler(event, context):
	# S3 bucket names
	INPUT_BUCKET_NAME = "YOUR INPUT BUCKET NAME"
	OUTPUT_BUCKET_NAME = "YOUR OUTPUT BUCKET NAME"

	# Get the S3 bucket and key from the event
	object_key = event['Records'][0]['s3']['object']['key']
	
	# specify the temp directory to store input, output and intermediate files
	temp_dir = "/tmp"

	# file path to download the video file to
	input_file_path = os.path.join(temp_dir, object_key)

	# download the video file from the S3 bucket to local storage
	is_downloaded = download_video_file(INPUT_BUCKET_NAME, object_key, input_file_path)

	# check if the video file was downloaded successfully
	if not is_downloaded:
		print("Error downloading video file!")
		return {
			'statusCode': 500,
			'body': json.dumps(f'Error downloading video file for input: {object_key}')
		}

	# process the video file and get recognized face name
	result_name = process_video(input_file_path, temp_dir)
	
	# pull academic information from DynamoDB
	academic_info = get_academic_info(result_name)

	# check if academic information is found
	if academic_info is None:
		print("No academic information found!")
		return {
			'statusCode': 500,
			'body': json.dumps(f'Error getting academic information for input: {object_key}')
		}

	# write the results to a output csv file
	write_results(object_key, academic_info, temp_dir)

	# upload the output file to S3 bucket
	upload_file(OUTPUT_BUCKET_NAME, object_key, temp_dir)

	return {
		'statusCode': 200,
		'body': json.dumps(f'Successfully processed input: {object_key}')
	}
import paramiko
import os
from tqdm import tqdm

def upload_to_hpc(local_path, remote_path, hostname, username, password=None, key_filename=None):
    """
    上传文件夹到HPC平台
    
    参数:
    local_path: 本地yolov7文件夹路径
    remote_path: HPC上的目标路径
    hostname: HPC主机名
    username: HPC用户名
    password: SSH密码（如果使用密码认证）
    key_filename: SSH密钥文件路径（如果使用密钥认证）
    """
    try:
        # 创建SSH客户端
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # 连接到HPC
        if password:
            ssh.connect(hostname, username=username, password=password)
        else:
            ssh.connect(hostname, username=username, key_filename=key_filename)
        
        # 创建SFTP客户端
        sftp = ssh.open_sftp()
        
        # 确保远程目录存在
        try:
            sftp.mkdir(remote_path)
        except IOError:
            pass  # 目录已存在
        
        # 遍历本地文件夹
        for root, dirs, files in os.walk(local_path):
            # 计算相对路径
            relative_path = os.path.relpath(root, local_path)
            remote_dir = os.path.join(remote_path, relative_path)
            
            # 创建远程目录
            try:
                sftp.mkdir(remote_dir)
            except IOError:
                pass  # 目录已存在
            
            # 上传文件
            for file in files:
                local_file = os.path.join(root, file)
                remote_file = os.path.join(remote_dir, file)
                
                # 显示进度
                print(f"Uploading: {local_file} -> {remote_file}")
                sftp.put(local_file, remote_file)
        
        print("Upload completed successfully!")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
    
    finally:
        # 关闭连接
        sftp.close()
        ssh.close()

if __name__ == "__main__":
    # 配置参数
    LOCAL_PATH = "/Users/sinmfull/yolov7"  # 修改为您的yolov7文件夹路径
    REMOTE_PATH = "/home/svu/e1352334/yolov7"    # 修改为HPC上的目标路径
    HOSTNAME = "atlas9.nus.edu.sg"            # 修改为您的HPC主机名
    USERNAME = "e1352334"              # 修改为您的HPC用户名
    
    # 选择认证方式（使用密码或密钥）
    # 方式1：使用密码
    PASSWORD = "Sinmfull0228"              # 修改为您的密码
    upload_to_hpc(LOCAL_PATH, REMOTE_PATH, HOSTNAME, USERNAME, password=PASSWORD)
    
    # 方式2：使用SSH密钥
    # KEY_FILE = "~/.ssh/id_rsa"           # 修改为您的SSH密钥文件路径
    # upload_to_hpc(LOCAL_PATH, REMOTE_PATH, HOSTNAME, USERNAME, key_filename=KEY_FILE)
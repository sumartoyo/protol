from os import path, makedirs
import tempfile
from importlib.machinery import SourceFileLoader
import hashlib
from grpc_tools import protoc

def load(proto_file):
    proto_dir = path.dirname(proto_file)
    proto_base = path.basename(proto_file)
    proto_name = proto_base[:-6]
    pb2_name = '{}_pb2'.format(proto_name)
    pb2_grpc_name = '{}_pb2_grpc'.format(proto_name)

    sha256 = hashlib.sha256()
    with open(proto_file, 'r') as f:
        sha256.update(f.read().encode('utf-16be'))
    checksum = sha256.hexdigest()[:7]

    compiled_dir = path.join(tempfile.gettempdir(), 'protol', '{}_{}'.format(proto_name, checksum))
    pb2_file = path.join(compiled_dir, '{}.py'.format(pb2_name))
    pb2_grpc_file = path.join(compiled_dir, '{}.py'.format(pb2_grpc_name))

    if path.isdir(compiled_dir):
        if path.exists(pb2_file) and path.exists(pb2_grpc_file):
            return (
                SourceFileLoader(pb2_name, pb2_file).load_module(),
                SourceFileLoader(pb2_grpc_name, pb2_grpc_file).load_module()
            )
    else:
        makedirs(compiled_dir)

    proto_include = protoc.pkg_resources.resource_filename('grpc_tools', '_proto')
    compile_arguments = [
        '-I{}'.format(proto_dir),
        '--proto_path={}'.format(proto_dir),
        '--python_out={}'.format(compiled_dir),
        '--grpc_python_out={}'.format(compiled_dir),
        proto_file,
        '-I{}'.format(proto_include)
    ]
    protoc.main(compile_arguments)

    return (
        SourceFileLoader(pb2_name, pb2_file).load_module(),
        SourceFileLoader(pb2_grpc_name, pb2_grpc_file).load_module()
    )

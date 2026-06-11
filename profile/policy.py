import yaml
from py_landlock import Landlock, AccessFs
from pathlib import Path
import enum
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_POLICY_FILE = os.path.join(PROJECT_ROOT, "profile", "policy.yaml")

def apply_security_policy(path):
    global _POLICY_FILE
    try:
        if path:
            _POLICY_FILE = str(path)
            policy = FileSystemPolicy()
            policy.load_file(path)
            policy.apply()
        else:
            print("[policy.apply_security_policy]: securityPolicyPath is not set")
    except Exception as e:
        print(f"[policy.apply_security_policy]: Unexpected exception: {repr(e)}")
        raise

class LandLockCompatibility(enum.Enum):
    BEST_EFFORT = 0
    HARD_REQUIREMENT = 1

class FileSystemPolicy:

    READ_ONLY_DIR_ACCESS = AccessFs.READ_DIR | AccessFs.READ_FILE
    READ_ONLY_FILE_ACCESS = AccessFs.READ_FILE
    READ_WRITE_DIR_ACCESS = (AccessFs.READ_FILE | AccessFs.READ_DIR
                             | AccessFs.WRITE_FILE | AccessFs.TRUNCATE
                             | AccessFs.MAKE_REG | AccessFs.MAKE_DIR
                             | AccessFs.MAKE_SYM | AccessFs.REMOVE_FILE
                             | AccessFs.REMOVE_DIR | AccessFs.MAKE_FIFO
                             | AccessFs.MAKE_SOCK)
    READ_WRITE_FILE_ACCESS = (AccessFs.READ_FILE | AccessFs.WRITE_FILE |
                              AccessFs.TRUNCATE)

    def __init__(self):
        self._strict = LandLockCompatibility.BEST_EFFORT
        self._read_only = []
        self._read_write = []

    def load_file(self, path: str|Path):
        print(f"[FileSystemPolicy.load_file] loading policy from file {path}")
        policy = None
        with open(path, "r") as f:
            policy = yaml.safe_load(f)
        self.load_dict(policy)

    def load_str(self, policy: str):
        policy = yaml.safe_load(policy)
        self.load_dict(policy)

    def load_dict(self, policy: dict):
        version = policy.get('version')
        assert version == 1

        self._strict = LandLockCompatibility.BEST_EFFORT
        ll = policy.get('landlock')
        if ll:
            comp = ll.get('compatibility')
            if comp:
                self._strict = LandLockCompatibility[comp.upper()]

        fs = policy.get('filesystem_policy')

        ro = []
        rw = []
        if fs:
            ro = fs.get('read_only', [])
            if ro is None:
                ro = []
            rw = fs.get('read_write', [])
            if rw is None:
                ro = []
            if policy.get('include_workdir'):
                rw.append(os.getcwd())
        self._read_only = [Path(f'{p}') for p in ro]
        self._read_write = [Path(f'{p}') for p in rw]

    def apply(self):
        ro = list(filter(lambda p: p.exists(), self._read_only))
        rw = list(filter(lambda p: p.exists(), self._read_write))
        rod = list(filter(lambda p: p.is_dir(), ro))
        rof = list(filter(lambda p: not p.is_dir(), ro))
        rwd = list(filter(lambda p: p.is_dir(), rw))
        rwf = list(filter(lambda p: not p.is_dir(), rw))

        strict = self._strict == LandLockCompatibility.HARD_REQUIREMENT
        Landlock(strict=strict) \
            .allow_all_scope() \
            .allow_all_network() \
            .add_path_rule('/', access=AccessFs.EXECUTE) \
            .add_path_rule(*rwd, access=FileSystemPolicy.READ_WRITE_DIR_ACCESS) \
            .add_path_rule(*rwf, access=FileSystemPolicy.READ_WRITE_FILE_ACCESS) \
            .add_path_rule(*rod, access=FileSystemPolicy.READ_ONLY_DIR_ACCESS) \
            .add_path_rule(*rof, access=FileSystemPolicy.READ_ONLY_FILE_ACCESS) \
            .apply()

        print("[FileSystemPolicy.load_file] policy applied")


POLICY_ALLOW = "POLICY_ALLOW"

class AgentPathPolicy:

    def __init__(self, read_protected=None, write_protected=None, root=None):
        self._root = root or PROJECT_ROOT
        self._read_protected = [self._to_abs(p) for p in (read_protected or [])]
        self._write_protected = [self._to_abs(p) for p in (write_protected or [])]

    def _to_abs(self, p):
        p = os.path.expanduser(str(p))
        if not os.path.isabs(p):
            p = os.path.join(self._root, p)
        return os.path.normpath(p)

    def _candidates(self, path):
        raw = os.path.expanduser(str(path).strip().strip('"'))
        bases = [raw] if os.path.isabs(raw) else [
            os.path.join(self._root, raw),
            os.path.join(os.getcwd(), raw),
        ]
        cands = set()
        for b in bases:
            cands.add(os.path.normpath(b))
            cands.add(os.path.realpath(b))
        return cands

    @staticmethod
    def _within(cand, protected):
        return cand == protected or cand.startswith(protected + os.sep)

    def _match(self, path, protected_list):
        for cand in self._candidates(path):
            for prot in protected_list:
                if self._within(cand, prot):
                    return prot
        return None

    def check_read(self, path):
        hit = self._match(path, self._read_protected)
        if hit:
            return f"POLICY_DENIED: reading '{path}' is blocked by the security policy"
        return POLICY_ALLOW

    def check_write(self, path):
        hit = self._match(path, self._write_protected)
        if hit:
            return f"POLICY_DENIED: writing '{path}' is blocked by the security policy"
        return POLICY_ALLOW


_AGENT_POLICY = None

def _load_agent_policy():
    global _AGENT_POLICY
    if _AGENT_POLICY is None:
        read_protected, write_protected = [], []
        try:
            with open(_POLICY_FILE, "r") as f:
                doc = yaml.safe_load(f) or {}
            section = doc.get("agent_path_policy") or {}
            read_protected = section.get("read_protected") or []
            write_protected = section.get("write_protected") or []
        except Exception as e:
            print(f"[policy._load_agent_policy]: {repr(e)}")
        _AGENT_POLICY = AgentPathPolicy(read_protected, write_protected)
    return _AGENT_POLICY

def check_path_read(path):
    return _load_agent_policy().check_read(path)

def check_path_write(path):
    return _load_agent_policy().check_write(path)

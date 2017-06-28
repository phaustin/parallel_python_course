from pathlib import Path
test_path=Path('..')
test_dir=test_path.resolve()
import site
site.addsitedir(str(test_dir))
from tests import test_pha


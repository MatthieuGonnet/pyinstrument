import django.template.loader
import django.conf
from timeit import Timer
import sys
import profile
import cProfile
import pyinstrument

sys.path.append('django_test')
django.conf.settings.configure(INSTALLED_APPS=(), TEMPLATE_DIRS=('./examples',))

def test_func_template():
    django.template.loader.render_to_string('template.html')

t = Timer(stmt=test_func_template)
test_func = lambda: t.repeat(number=200)

# base
base_timings = test_func()

# # profile
# p = profile.Profile()
# profile_timings = p.runcall(lambda: test_func())

# cProfile
cp = cProfile.Profile()
cProfile_timings = cp.runcall(test_func)

# pyinstrument stat
profiler = pyinstrument.Profiler()
profiler.start()
pyinstrument_timings = test_func()
profiler.stop()

# pyinstrument stat
profiler = pyinstrument.Profiler(timeline=True)
profiler.start()
pyinstrument_timeline_timings = test_func()
profiler.stop()

with open('out.html', 'w') as f:
    f.write(profiler.output_html())

print(profiler.output_text(unicode=True, color=True))

graph_data = (
    ('Base timings', min(base_timings)),
    # ('profile', min(profile_timings)),
    ('cProfile', min(cProfile_timings)),
    ('pyinstrument', min(pyinstrument_timings)),
    ('pyinstrument timeline', min(pyinstrument_timeline_timings)),
)

from ascii_graph import Pyasciigraph

graph = Pyasciigraph()
for line in graph.graph('Profiler overhead', graph_data):
    print(line)

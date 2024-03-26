# Programming blog

```bash
pip install django-taggit
```


```python
from taggit.managers import TaggableManager

class Post(models.Model):
    tags = TaggableManager()

```

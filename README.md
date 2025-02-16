# TDS-project-1

run datagen.py using

```bash
 uv run datagen.py 22xxxxxx@ds.study.iitm.ac.in --root ./data
```

then run taskA.py

```bash
uv run tasksA.py
```

then start the server using

```bash
uvicorn server:app --reload
```

then run the evaluate script

```bash
uv run evaluate.py --email=22xxxxxxx@ds.study.iitm.ac.in --log-level=INFO
```

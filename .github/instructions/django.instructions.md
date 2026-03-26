---
description: "Django coding conventions and best practices. Use when writing, reviewing, or refactoring Django applications."
applyTo: "**/*.py"
---

# Django Conventions

- Always set `on_delete` explicitly on `ForeignKey` and `OneToOneField` — use `CASCADE` for owned children, `PROTECT` for referenced lookups, `SET_NULL` (with `null=True`) for optional associations. Never use `on_delete=models.DO_NOTHING`
- Define a `Meta` class on every model with at least `ordering`, `verbose_name`, and `verbose_name_plural`. Add `constraints` and `indexes` in `Meta` instead of field-level `db_index=True` for compound indexes
- Use `select_related()` for `ForeignKey`/`OneToOneField` joins and `prefetch_related()` for reverse relations and `ManyToManyField`. Profile queries with `django-debug-toolbar` or `assertNumQueries` in tests to catch N+1
- Use `F()` expressions for database-level field references in updates and annotations — never read a field into Python just to write it back (e.g., `Model.objects.filter(...).update(count=F('count') + 1)`)
- Use `Q()` objects for complex lookups with `OR`, `NOT`, or nested boolean logic. Combine with `&`, `|`, `~` operators — never use raw SQL for conditions expressible with the ORM
- Use `.values()` or `.values_list()` when you only need specific columns — avoid loading full model instances for read-only aggregate or export queries
- Prefer class-based views (`ListView`, `DetailView`, `CreateView`, `UpdateView`) for standard CRUD. Use function-based views only for non-standard flows or when CBV mixins become convoluted
- Apply `LoginRequiredMixin` or `PermissionRequiredMixin` as the first parent in CBV inheritance order. For FBVs use `@login_required` and `@permission_required` decorators. Never check `request.user.is_authenticated` manually in views that have a mixin/decorator available
- Define URL patterns in per-app `urls.py` modules and include them in the root `urlconf` with `app_name` for namespacing. Use `reverse()` or `{% url %}` with namespace — never hardcode URL paths
- Write custom middleware as a function-based middleware (ASGI/WSGI compatible) or class with `__init__`/`__call__`. Keep middleware thin — delegate logic to services. Order middleware carefully: security middleware first, auth before permission checks
- Use signals sparingly — only for decoupled cross-app notifications (e.g., `post_save` for audit logging). Never use signals for same-app business logic; call service functions directly instead
- Use Django REST Framework serializers for API input validation and output shaping. Use `ModelSerializer` for standard CRUD, `Serializer` for custom shapes. Always set `fields` explicitly — never use `fields = '__all__'`
- Validate at the model level with `clean()` and field validators so validation runs on both form and API paths. Raise `ValidationError` with a message dict keyed by field name
- Always review auto-generated migrations before committing. Never hand-edit auto-migrations — create a separate manual migration with `RunPython` or `RunSQL` for data migrations. Squash migrations periodically in long-lived apps
- Register every model in `admin.py` with at least `list_display`, `search_fields`, and `list_filter`. Use `readonly_fields` for computed/audit fields. Override `get_queryset` to add `select_related` for admin list views
- Use Django's template engine only for server-rendered pages. Avoid complex logic in templates — move it to template tags, filters, or view context. Never call methods with side effects from templates
- Rely on Django's built-in CSRF protection — never use `@csrf_exempt` unless the endpoint is a webhook with its own signature verification. Use `{% csrf_token %}` in all HTML forms
- Use Django's ORM parameterized queries exclusively. Never interpolate user input into raw SQL. If `raw()` or `extra()` is unavoidable, use params — never f-strings or `.format()`
- Structure settings with `django-environ` for environment variable parsing. Split into `base.py`, `development.py`, `production.py`, and `testing.py` that import from base. Never commit secrets to settings files
- Use Django's cache framework (`django.core.cache`) with a backend like Redis. Cache expensive querysets and computed values. Use `@cache_page` for full-page caching and `cache.get_or_set()` for fragment caching. Always set explicit timeouts
- Define Celery tasks in per-app `tasks.py` files. Use `@shared_task` decorator. Set `acks_late=True` and `reject_on_worker_lost=True` for critical tasks. Always set `time_limit` and `soft_time_limit` on tasks to prevent runaway workers
- Use `django.test.TestCase` for tests that need database access and `SimpleTestCase` for tests that don't. Use DRF's `APITestCase` for API endpoint tests. Prefer `factory_boy` over fixtures for test data setup
- Define custom managers on models for reusable query logic (e.g., `PublishedManager` with `.get_queryset().filter(status='published')`). Attach as `objects` or a secondary manager — keep the default manager unfiltered
- Use `FileField` or `ImageField` with a custom `upload_to` callable for organized storage. Validate file type and size in the model's `clean()` method. Serve user uploads through a CDN or dedicated media server — never from the app server in production
- Use Django's `Paginator` for server-rendered pages and DRF's `PageNumberPagination` or `CursorPagination` for APIs. Always paginate list endpoints — never return unbounded querysets
- Use `transaction.atomic()` as a context manager for operations that must succeed or fail together. Avoid nesting `atomic()` blocks — use `savepoint=False` if nesting is unavoidable
- Use `django.utils.timezone.now()` instead of `datetime.now()` or `datetime.utcnow()`. Store all timestamps in UTC. Set `USE_TZ = True` in settings — never disable timezone support
- Use `CharField` with `choices` for small fixed sets, or a separate model with `ForeignKey` for large/dynamic option sets. In Django 5+, use `GeneratedField` for database-level computed columns instead of `@property` for frequently queried derived values
- Use `unique_together` or `UniqueConstraint` in `Meta.constraints` for composite uniqueness. Prefer `CheckConstraint` for database-level business rule enforcement over application-only validation
- Use `django.contrib.auth.get_user_model()` to reference the user model — never import `User` directly. Define a custom user model extending `AbstractUser` or `AbstractBaseUser` at project start, even if the default fields suffice
- For Django 5+ async views, use `async def` view functions with `async for` on querysets and `await` on ORM calls (`aget`, `afilter`, `acreate`, etc.). Never mix sync ORM calls inside async views — use `sync_to_async` only as a last resort
- Use `manage.py check --deploy` before every production deployment to catch common security misconfigurations. Ensure `SECURE_SSL_REDIRECT`, `SECURE_HSTS_SECONDS`, `SESSION_COOKIE_SECURE`, and `CSRF_COOKIE_SECURE` are all enabled in production settings
- Define `__str__` on every model returning a human-readable representation. Define `get_absolute_url()` on models that have a detail page. Use these consistently in admin, templates, and logs
- Use `django.core.mail.send_mail` with a configurable backend — never call SMTP directly. Use `django-anymail` for production email services. Always send email asynchronously via Celery in production
- Use `LogEntry` or `django-auditlog` for tracking model changes. Store the user, timestamp, and diff of changed fields. Never rely on signals alone for audit trails — signals can be bypassed by bulk operations

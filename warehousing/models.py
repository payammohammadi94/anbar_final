from statistics import mode
from unicodedata import category
from django.db import models

# Create your models here.
from django.db import models

from django.conf import settings
# Create your models here.
from django.db.models.signals import pre_delete
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length = 255)
    code = models.CharField(max_length = 20,null=True,blank=True)
    is_sub = models.BooleanField(default=False)
    sub_cat = models.ForeignKey('self',on_delete=models.CASCADE, verbose_name='زیر دسته بندی',related_name='catgory',blank=True,null=True)
    
    def __str__(self):
        return f"{self.name} + {self.code}"
    
    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی"

class ResponsibleForTesting(models.Model):
    first_last_name = models.CharField(max_length=255, verbose_name="نام و نام خانوادگی مسئول تست")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="ایجادکننده"
    )
    def __str__(self):
        return f"{self.first_last_name}"

    class Meta:
        verbose_name = "مسئول تست"
        verbose_name_plural = "مسئول تست"

class ResponsibleForQC(models.Model):
    first_last_name = models.CharField(max_length=255, verbose_name="نام و نام خانوادگی مسئول QC")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="ایجادکننده"
    )
    def __str__(self):
        return f"{self.first_last_name}"

    class Meta:
        verbose_name = "مسئول QC"
        verbose_name_plural = "مسئول QC"

class ProductPart(models.Model):
    product_part = models.CharField(max_length=255, verbose_name="پارت کالا")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="ایجادکننده"
    )
    def __str__(self):
        return f"{self.product_part}"

    class Meta:
        verbose_name = "پارت کالا"
        verbose_name_plural = "پارت کالا"

class ProductCode(models.Model):
    product_code = models.CharField(max_length=255, verbose_name="کد کالا")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="ایجادکننده"
    )
    def __str__(self):
        return f"{self.product_code}"

    class Meta:
        verbose_name = "کد کالا"
        verbose_name_plural = "کد کالا"

class QuarantineWarehouse(models.Model):
    DESTINATION_CHOICES = [
    ('raw_material', 'انبار مواد اولیه'),
    ('returned', 'محصول بازگشتی'),
    ]
    STATUS_CHOICES = [
        ('waiting_test', 'در انتظار تست'),
        ('testing', 'در حال تست'),
        ('testing_done', 'تست شده'),
        ('qc_pending', 'در انتظار QC'),
        ('approved', 'تایید شده'),
        ('rejected', 'رد شده'),
        ('transferred', 'موجود در انبار اولیه'),
        ('used_in_product', 'استفاده شده در محصول'),
        ('used_in_secondry_warehouse', 'استفاده شده در انبار ثانویه'),
        ('inCompany', 'تحویل افراد شرکت'),
        ('outCompany', 'امانی شرکت به بیرون'),
    ]
    
    STATUS_AMANI_CHOICES = [
        ('YES', 'امانی هست'),
        ('NO', 'امانی نیست'),
    ]
    UNIT_PRICE_CHOICES = [
        ('dollar','دلار'),
        ('toman','تومان')
    ]

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="ایجادکننده"
    )
    status_amani = models.CharField(max_length=50, choices=STATUS_AMANI_CHOICES, default='NO', verbose_name="وضعیت امانی")
    piece_name = models.CharField(max_length=255, verbose_name="نام قطعه")
    category = models.ManyToManyField(Category,blank=True,verbose_name='دسته‌بندی',related_name='category_rel')
    part_number = models.ForeignKey(ProductPart, on_delete=models.CASCADE, null=True, blank=True, verbose_name="پارت کالا")
    item_code = models.ForeignKey(ProductCode, on_delete=models.CASCADE, verbose_name="کد کالا")
    quantity = models.IntegerField(blank=True, null=True, verbose_name="تعداد")
    Meterage = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="(متر)متراژ", blank=True, null=True)
    entry_date = models.DateField(verbose_name="تاریخ ورود")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="قیمت")
    unit = models.CharField(max_length=50, verbose_name="واحد", choices=UNIT_PRICE_CHOICES)
    supplier = models.CharField(max_length=255, verbose_name="تامین کننده")
    serial_number = models.CharField(max_length=255, blank=True, null=True, verbose_name="شماره سریال")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='waiting_test', verbose_name="وضعیت قطعه")
    qc_date = models.DateField(blank=True, null=True, verbose_name="تاریخ QC")
    qc_responsible = models.ForeignKey(ResponsibleForQC,blank=True, null=True, verbose_name="مسئول QC", on_delete=models.CASCADE,)
    # qc_responsible = models.CharField(max_length=255, blank=True, null=True, verbose_name="مسئول QC")
    qc_description = models.TextField(blank=True, null=True, verbose_name="شرح QC")
    test_date = models.DateField(blank=True, null=True, verbose_name="تاریخ تست")
    test_responsible = models.ForeignKey(ResponsibleForTesting,blank=True, null=True, verbose_name="مسئول تست",on_delete=models.CASCADE,)
    # test_responsible = models.CharField(max_length=255, blank=True, null=True, verbose_name="مسئول تست")
    test_description = models.TextField(blank=True, null=True, verbose_name="شرح تست")
    exit_date = models.DateField(blank=True, null=True, verbose_name="تاریخ خروج")
    destination = models.CharField(max_length=50, choices=DESTINATION_CHOICES, blank=True, null=True, verbose_name="مقصد")


    def __str__(self):
        return f"{self.piece_name} ({self.item_code})"

    class Meta:
        verbose_name = "موجودیت انبار قرنطینه"
        verbose_name_plural = "انبار قرنطینه"

class RawMaterialWarehouse(models.Model):
    UNIT_PRICE_CHOICES = [
        ('dollar','دلار'),
        ('toman','تومان')
    ]
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="ایجادکننده"
    )
    quarantine_reference = models.ForeignKey(QuarantineWarehouse, on_delete=models.CASCADE, null=True, blank=True, verbose_name="ارجاع به قرنطینه")
    category = models.ManyToManyField(Category,blank=True,verbose_name='دسته‌بندی',related_name='category_rel_raw')
    piece_name = models.CharField(max_length=255, verbose_name="نام قطعه")
    part_number = models.ForeignKey(ProductPart, on_delete=models.CASCADE, null=True, blank=True, verbose_name="پارت کالا")
    item_code = models.ForeignKey(ProductCode, on_delete=models.CASCADE, null=True, blank=True, verbose_name="کد کالا")
    quantity = models.IntegerField(verbose_name="تعداد")
    entry_date = models.DateField(verbose_name="تاریخ ورود")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="قیمت")
    unit = models.CharField(max_length=50, verbose_name="واحد",choices=UNIT_PRICE_CHOICES)
    serial_number = models.CharField(max_length=255, blank=True, null=True, verbose_name="شماره سریال")

    def __str__(self):
        return f"{self.piece_name} - {self.serial_number} - {self.item_code} - {self.part_number}"

    class Meta:
        verbose_name = "موجودیت انبار مواد اولیه"
        verbose_name_plural = "انبار مواد اولیه"

class ProductWarehouse(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="ایجادکننده"
    )
    STATUS_CHOICES = [
        ('product_warehouse', 'انبار محصولات'),
        ('internal_product', 'تحویل افراد درون شرکت'),
        ('out_product', 'امانی شرکت به بیرون'),
        ('seller_product', 'فروخته شده'),
    ]
    product_name = models.CharField(max_length=255, verbose_name="محصول")
    quantity = models.IntegerField(blank=True, null=True, verbose_name="تعداد",default=1)
    product_serial_number = models.CharField(max_length=255, unique=True, verbose_name="شماره سریال محصول")
    manufacturing_start_date = models.DateField(verbose_name="تاریخ شروع ساخت")
    manufacturing_end_date = models.DateField(blank=True, null=True, verbose_name="تاریخ اتمام ساخت")
    test_qc_start_date = models.DateField(blank=True, null=True, verbose_name="تاریخ شروع تست و QC")
    qc_responsible = models.CharField(max_length=255, blank=True, null=True, verbose_name="مسئول QC")
    test_approver = models.CharField(max_length=255, blank=True, null=True, verbose_name="تایید کننده تست")
    test_qc_end_date = models.DateField(blank=True, null=True, verbose_name="تاریخ پایان تست و QC")
    product_exit_date = models.DateField(blank=True, null=True, verbose_name="تاریخ خروج محصول")
    exit_type = models.CharField(max_length=255, blank=True, null=True, verbose_name="نوع خروج")
    deliverer = models.CharField(max_length=255, blank=True, null=True, verbose_name="تحویل دهنده")
    receiver = models.CharField(max_length=255, blank=True, null=True, verbose_name="تحویل گیرنده")
    finished_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="قیمت تمام شده")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='product_warehouse', verbose_name="وضعیت محصول")

    def __str__(self):
        return f"{self.product_name} - {self.product_serial_number}"

    class Meta:
        verbose_name = "موجودیت انبار محصولات"
        verbose_name_plural = "انبار محصولات"

class ReturnedProduct(models.Model):
    UNIT_PRICE_CHOICES = [
        ('dollar','دلار'),
        ('toman','تومان')
    ]
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="ایجادکننده"
    )
    piece_name = models.CharField(max_length=255, verbose_name="نام قطعه")
    part_number = models.ForeignKey(ProductPart, on_delete=models.CASCADE, null=True, blank=True, verbose_name="پارت کالا")
    item_code = models.ForeignKey(ProductCode, on_delete=models.CASCADE, null=True, blank=True, verbose_name="کد کالا")
    supplier = models.CharField(max_length=255, blank=True, null=True, verbose_name="تامین کننده")
    return_date = models.DateField(verbose_name="تاریخ بازگشت")
    reason_for_return = models.TextField(verbose_name="دلیل بازگشت")
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="قیمت")
    unit = models.CharField(max_length=50, blank=True, null=True, verbose_name="واحد", choices=UNIT_PRICE_CHOICES)
    serial_number = models.CharField(max_length=255, blank=True, null=True, verbose_name="شماره سریال")

    def __str__(self):
        return f"بازگشتی: {self.piece_name} ({self.item_code})"

    class Meta:
        verbose_name = "محصول برگشتی به فروشنده"
        verbose_name_plural = "محصولات برگشتی به فروشنده"

class ProductRawMaterial(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="ایجادکننده"
    )
    product = models.ForeignKey(ProductWarehouse, on_delete=models.CASCADE, related_name='raw_materials', verbose_name="محصول")
    raw_material_source = models.ForeignKey(
        RawMaterialWarehouse, on_delete=models.CASCADE,
        null=True, blank=True, verbose_name="انتخاب از انبار مواد اولیه"
    )
    raw_material_name = models.CharField(max_length=255, verbose_name="ماده اولیه")
    part_number = models.ForeignKey(ProductPart, on_delete=models.CASCADE, null=True, blank=True, verbose_name="پارت کالا")
    item_code = models.ForeignKey(ProductCode, on_delete=models.CASCADE, null=True, blank=True, verbose_name="کد کالا")
    quantity = models.IntegerField(verbose_name="مقدار")
    user_who_used = models.CharField(max_length=255, verbose_name="استفاده کننده")
    raw_material_entry_date = models.DateField(verbose_name="تاریخ ورود ماده اولیه")
    raw_material_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="قیمت ماده اولیه")
    unit = models.CharField(max_length=50, verbose_name="واحد", choices=[
        ('dollar', 'دلار'),
        ('toman', 'تومان')
    ])
    serial_number = models.CharField(max_length=255, blank=True, null=True, verbose_name="شماره سریال")

    def save(self, *args, **kwargs):
        raw = self.raw_material_source
        # بررسی اینکه رکورد جدید است یا ویرایش شده
        if self.pk:
            old = ProductRawMaterial.objects.get(pk=self.pk)

            if old.raw_material_source == self.raw_material_source:
                diff = self.quantity - old.quantity

                if diff > 0:  # افزایش مصرف
                    if raw and raw.quantity >= diff:
                        raw.quantity -= diff
                        raw.save()
                    else:
                        raise ValueError("مقدار جدید بیشتر از موجودی انبار است.")
                elif diff < 0:  # کاهش مصرف
                    if raw:
                        raw.quantity += abs(diff)
                        raw.save()
            else:
                # منبع تغییر کرده
                if old.raw_material_source:
                    old.raw_material_source.quantity += old.quantity
                    old.raw_material_source.save()
                if raw:
                    if raw.quantity >= self.quantity:
                        raw.quantity -= self.quantity
                        raw.save()
                    else:
                        raise ValueError("مقدار وارد شده بیشتر از موجودی انبار است.")
        else:
            # رکورد جدید است
            if raw:
                if raw.quantity >= self.quantity:
                    raw.quantity -= self.quantity
                    raw.save()
                else:
                    raise ValueError("مقدار وارد شده بیشتر از موجودی انبار است.")

        # پر کردن اطلاعات از منبع در صورت خالی بودن
        if raw and not self.raw_material_name:
            self.raw_material_name = raw.piece_name
            self.item_code = raw.item_code
            self.part_number = raw.part_number
            self.raw_material_entry_date = raw.entry_date
            self.raw_material_price = raw.price
            self.unit = raw.unit
            self.serial_number = raw.serial_number

        # وضعیت قرنطینه
        if raw and raw.quarantine_reference:
            raw.quarantine_reference.status = 'used_in_product'
            raw.quarantine_reference.save()

        super().save(*args, **kwargs)
    def delete(self, *args, **kwargs):
        if self.raw_material_source:
            self.raw_material_source.quantity += self.quantity
            self.raw_material_source.save()

            # بازگرداندن وضعیت قرنطینه اگر دیگر استفاده نشده باشد
            quarantine_ref = self.raw_material_source.quarantine_reference
            if quarantine_ref:
                others = ProductRawMaterial.objects.filter(
                    raw_material_source=self.raw_material_source
                ).exclude(pk=self.pk)

                if not others.exists():
                    quarantine_ref.status = 'transferred'
                    quarantine_ref.save()

        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.raw_material_name} for {self.product.product_name}"

    class Meta:
        verbose_name = "ماده اولیه محصول"
        verbose_name_plural = "مواد اولیه محصول"

class SecondryWarehouse(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="ایجادکننده"
    )
    STATUS_CHOICES = [
        ('secondry_warehouse', 'انبار ثانویه'),
        ('in_product', 'استفاده شده در محصول'),
        ('internal_product', 'تحویل افراد درون شرکت'),
        ('out_product', 'امانی شرکت به بیرون'),
        ('seller_product', 'فروخته شده'),
    ]
    product_name = models.CharField(max_length=255, verbose_name="محصول ثانویه")
    product_serial_number = models.CharField(max_length=255, unique=True, verbose_name="شماره سریال محصول ثانویه")
    manufacturing_start_date = models.DateField(verbose_name="تاریخ شروع ساخت")
    manufacturing_end_date = models.DateField(blank=True, null=True, verbose_name="تاریخ اتمام ساخت")
    test_qc_start_date = models.DateField(blank=True, null=True, verbose_name="تاریخ شروع تست و QC")
    test_qc_end_date = models.DateField(blank=True, null=True, verbose_name="تاریخ پایان تست و QC")
    test_approver = models.CharField(max_length=255, blank=True, null=True, verbose_name="تایید کننده تست")
    qc_responsible = models.CharField(max_length=255, blank=True, null=True, verbose_name="مسئول QC")
    product_exit_date = models.DateField(blank=True, null=True, verbose_name="تاریخ خروج محصول")
    exit_type = models.CharField(max_length=255, blank=True, null=True, verbose_name="نوع خروج")
    deliverer = models.CharField(max_length=255, blank=True, null=True, verbose_name="تحویل دهنده")
    receiver = models.CharField(max_length=255, blank=True, null=True, verbose_name="تحویل گیرنده")
    finished_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="قیمت تمام شده")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='secondry_warehouse', verbose_name="وضعیت محصول")

    def __str__(self):
        return f"{self.product_name} - {self.product_serial_number}"

    class Meta:
        verbose_name = "انبار ثانویه"
        verbose_name_plural = "انبار ثانویه"

class SecondryWarehouseRawMaterial(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="ایجادکننده"
    )
    secondryWarehouse = models.ForeignKey(SecondryWarehouse, on_delete=models.CASCADE, related_name='raw_materials', verbose_name="محصول انبار ثانویه")
    raw_material_source = models.ForeignKey(
        RawMaterialWarehouse, on_delete=models.CASCADE,
        null=True, blank=True, verbose_name="انتخاب از انبار مواد اولیه"
    )
    raw_material_name = models.CharField(max_length=255, verbose_name="ماده اولیه", null=True, blank=True)
    part_number = models.ForeignKey(ProductPart, on_delete=models.CASCADE, null=True, blank=True, verbose_name="پارت کالا")
    item_code = models.ForeignKey(ProductCode, on_delete=models.CASCADE, null=True, blank=True, verbose_name="کد کالا")
    serial_number = models.CharField(max_length=255, blank=True, null=True, verbose_name="شماره سریال")
    quantity = models.IntegerField(verbose_name="مقدار")
    user_who_used = models.CharField(blank=True, null=True, max_length=255, verbose_name="استفاده کننده")
    raw_material_entry_date = models.DateField(verbose_name="تاریخ ورود ماده اولیه", null=True, blank=True)
    raw_material_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="قیمت ماده اولیه", null=True, blank=True)
    unit = models.CharField(max_length=50, verbose_name="واحد", choices=[
        ('dollar', 'دلار'),
        ('toman', 'تومان')
    ], null=True, blank=True)

    def save(self, *args, **kwargs):
        raw = self.raw_material_source
        # بررسی اینکه رکورد جدید است یا ویرایش شده
        if self.pk:
            old = SecondryWarehouseRawMaterial.objects.get(pk=self.pk)

            if old.raw_material_source == self.raw_material_source:
                diff = self.quantity - old.quantity

                if diff > 0:  # افزایش مصرف
                    if raw and raw.quantity >= diff:
                        raw.quantity -= diff
                        raw.save()
                    else:
                        raise ValueError("مقدار جدید بیشتر از موجودی انبار است.")
                elif diff < 0:  # کاهش مصرف
                    if raw:
                        raw.quantity += abs(diff)
                        raw.save()
            else:
                # منبع تغییر کرده
                if old.raw_material_source:
                    old.raw_material_source.quantity += old.quantity
                    old.raw_material_source.save()
                if raw:
                    if raw.quantity >= self.quantity:
                        raw.quantity -= self.quantity
                        raw.save()
                    else:
                        raise ValueError("مقدار وارد شده بیشتر از موجودی انبار است.")
        else:
            # رکورد جدید است
            if raw:
                if raw.quantity >= self.quantity:
                    raw.quantity -= self.quantity
                    raw.save()
                else:
                    raise ValueError("مقدار وارد شده بیشتر از موجودی انبار است.")

        # پر کردن اطلاعات از منبع در صورت خالی بودن
        if raw and not self.raw_material_name:
            self.raw_material_name = raw.piece_name
            self.item_code = raw.item_code
            self.part_number = raw.part_number
            self.raw_material_entry_date = raw.entry_date
            self.raw_material_price = raw.price
            self.unit = raw.unit
            self.serial_number = raw.serial_number

        # وضعیت قرنطینه
        if raw and raw.quarantine_reference:     
            raw.quarantine_reference.status = 'used_in_secondry_warehouse'
            raw.quarantine_reference.save()

        super().save(*args, **kwargs)
    def delete(self, *args, **kwargs):
        if self.raw_material_source:
            self.raw_material_source.quantity += self.quantity
            self.raw_material_source.save()

            # بازگرداندن وضعیت قرنطینه اگر دیگر استفاده نشده باشد
            quarantine_ref = self.raw_material_source.quarantine_reference
            if quarantine_ref:
                others = SecondryWarehouseRawMaterial.objects.filter(
                    raw_material_source=self.raw_material_source
                ).exclude(pk=self.pk)

                if not others.exists():
                    quarantine_ref.status = 'transferred'
                    quarantine_ref.save()

        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.raw_material_name} for {self.secondryWarehouse.product_name}"

    class Meta:
        verbose_name = "مواد اولیه انبار ثانویه"
        verbose_name_plural = "مواد اولیه انبار ثانویه"

class ProductSecondryProduct(models.Model):
    product = models.ForeignKey(
        'ProductWarehouse',
        on_delete=models.CASCADE,
        related_name='secondry_products',
        verbose_name="محصول نهایی"
    )
    secondry_product = models.ForeignKey(
        SecondryWarehouse,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="محصول ثانویه مصرف‌شده"
    )
    quantity = models.IntegerField(verbose_name="تعداد مصرف‌ شده از محصول ثانویه")

    def __str__(self):
        return f"{self.secondry_product} در {self.product}"

    class Meta:
        verbose_name = "محصول ثانویه در محصول نهایی"
        verbose_name_plural = "محصولات ثانویه در محصول نهایی"

class ProductDelivery(models.Model):
    receiver_name = models.CharField(max_length=255, verbose_name="نام و نام خانوادگی تحویل گیرنده")
    user_name = models.CharField(blank=True, null=True,max_length=255, verbose_name="شناسه کاربری تحویل گیرنده")
    delivery_date = models.DateField(verbose_name="تاریخ تحویل")
    return_date = models.DateField(blank=True, null=True, verbose_name="تاریخ بازگشت")
    deliverer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="تحویل دهنده"
    )

    def __str__(self):
        return f"{self.receiver_name} - {self.delivery_date}"

    class Meta:
        verbose_name = "تحویل محصول به افراد داخل شرکت"
        verbose_name_plural = "تحویل محصولات به افراد داخل شرکت"

class ProductDeliveryProduct(models.Model):
    delivery = models.ForeignKey(ProductDelivery, on_delete=models.CASCADE, related_name="product_items")
    product = models.ForeignKey(ProductWarehouse, on_delete=models.CASCADE, null=True, blank=True, verbose_name="محصول")
    quantity = models.IntegerField(verbose_name="تعداد")
    delivery_date = models.DateField(blank=True, null=True, verbose_name="تاریخ تحویل")
    return_date = models.DateField(blank=True, null=True, verbose_name="تاریخ برگشت")
    
    def save(self, *args, **kwargs):
        product = self.product
        # بررسی اینکه رکورد جدید است یا ویرایش شده
        if self.pk:
            old = ProductDeliveryProduct.objects.get(pk=self.pk)

            if old.product == self.product:
                diff = self.quantity - old.quantity

                if diff > 0:  # افزایش مصرف
                    if product and product.quantity >= diff:
                        product.quantity -= diff
                        product.save()
                    else:
                        raise ValueError("مقدار جدید بیشتر از موجودی انبار است.")
                elif diff < 0:  # کاهش مصرف
                    if product:
                        product.quantity += abs(diff)
                        product.save()
            else:
                # منبع تغییر کرده
                if old.product:
                    old.product.quantity += old.quantity
                    old.product.save()
                if product:
                    if product.quantity >= self.quantity:
                        product.quantity -= self.quantity
                        product.save()
                    else:
                        raise ValueError("مقدار وارد شده بیشتر از موجودی انبار است.")
        else:
            # رکورد جدید است
            if product:
                if product.quantity >= self.quantity:
                    product.quantity -= self.quantity
                    product.save()
                else:
                    raise ValueError("مقدار وارد شده بیشتر از موجودی انبار است.")

        # بررسی بازگشت محصول
        if self.pk:  # فقط برای رکوردهای موجود
            old = ProductDeliveryProduct.objects.get(pk=self.pk)
            # اگر تاریخ برگشت اضافه شده و قبلاً خالی بوده
            if self.return_date and not old.return_date:
                # بازگرداندن موجودی به انبار محصولات
                if product:
                    product.quantity += self.quantity
                    # تغییر وضعیت به انبار محصولات
                    product.status = 'product_warehouse'
                    product.save()
                    # صفر کردن تعداد در این کلاس
                    self.quantity = 0
            # اگر تاریخ برگشت حذف شده و قبلاً پر بوده
            elif not self.return_date and old.return_date:
                # دوباره کم کردن موجودی از انبار محصولات
                if product and product.quantity >= self.quantity:
                    product.quantity -= self.quantity
                    # تغییر وضعیت به تحویل داخلی
                    product.status = 'internal_product'
                    product.save()
                else:
                    raise ValueError("موجودی انبار کافی نیست.")
        else:
            # تغییر وضعیت محصول به تحویل داخلی (فقط برای رکوردهای جدید)
            if product:
                product.status = 'internal_product'
                product.save()

        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        if self.product:
            self.product.quantity += self.quantity
            # بازگرداندن وضعیت محصول به انبار محصولات
            self.product.status = 'product_warehouse'
            self.product.save()

        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.product.product_name if self.product else 'محصول'} for {self.delivery.receiver_name}"

    class Meta:
        verbose_name = "محصولات تحویل افراد"
        verbose_name_plural = "محصولات تحویل افراد"
class ProductDeliverySecondryProduct(models.Model):
    delivery = models.ForeignKey(ProductDelivery, on_delete=models.CASCADE, related_name="secondry_items")
    secondry_product = models.ForeignKey(SecondryWarehouse, on_delete=models.CASCADE, null=True, blank=True, verbose_name="محصول ثانویه")
    quantity = models.IntegerField(verbose_name="تعداد")
    delivery_date = models.DateField(blank=True, null=True, verbose_name="تاریخ تحویل")
    return_date = models.DateField(blank=True, null=True, verbose_name="تاریخ برگشت")

    def save(self, *args, **kwargs):
        secondry_product = self.secondry_product
        # بررسی اینکه رکورد جدید است یا ویرایش شده
        if self.pk:
            old = ProductDeliverySecondryProduct.objects.get(pk=self.pk)

            if old.secondry_product == self.secondry_product:
                diff = self.quantity - old.quantity

                if diff > 0:  # افزایش مصرف
                    if secondry_product and secondry_product.quantity >= diff:
                        secondry_product.quantity -= diff
                        secondry_product.save()
                    else:
                        raise ValueError("مقدار جدید بیشتر از موجودی انبار است.")
                elif diff < 0:  # کاهش مصرف
                    if secondry_product:
                        secondry_product.quantity += abs(diff)
                        secondry_product.save()
            else:
                # منبع تغییر کرده
                if old.secondry_product:
                    old.secondry_product.quantity += old.quantity
                    old.secondry_product.save()
                if secondry_product:
                    if secondry_product.quantity >= self.quantity:
                        secondry_product.quantity -= self.quantity
                        secondry_product.save()
                    else:
                        raise ValueError("مقدار وارد شده بیشتر از موجودی انبار است.")
        else:
            # رکورد جدید است
            if secondry_product:
                if secondry_product.quantity >= self.quantity:
                    secondry_product.quantity -= self.quantity
                    secondry_product.save()
                else:
                    raise ValueError("مقدار وارد شده بیشتر از موجودی انبار است.")

        # بررسی بازگشت محصول ثانویه
        if self.pk:  # فقط برای رکوردهای موجود
            old = ProductDeliverySecondryProduct.objects.get(pk=self.pk)
            # اگر تاریخ برگشت اضافه شده و قبلاً خالی بوده
            if self.return_date and not old.return_date:
                # بازگرداندن موجودی به انبار ثانویه
                if secondry_product:
                    secondry_product.quantity += self.quantity
                    # تغییر وضعیت به انبار ثانویه
                    secondry_product.status = 'secondry_warehouse'
                    secondry_product.save()
                    # صفر کردن تعداد در این کلاس
                    self.quantity = 0
            # اگر تاریخ برگشت حذف شده و قبلاً پر بوده
            elif not self.return_date and old.return_date:
                # دوباره کم کردن موجودی از انبار ثانویه
                if secondry_product and secondry_product.quantity >= self.quantity:
                    secondry_product.quantity -= self.quantity
                    # تغییر وضعیت به تحویل داخلی
                    secondry_product.status = 'internal_product'
                    secondry_product.save()
                else:
                    raise ValueError("موجودی انبار کافی نیست.")
        else:
            # تغییر وضعیت محصول ثانویه به تحویل داخلی (فقط برای رکوردهای جدید)
            if secondry_product:
                secondry_product.status = 'internal_product'
                secondry_product.save()

        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        if self.secondry_product:
            self.secondry_product.quantity += self.quantity
            # بازگرداندن وضعیت محصول ثانویه به انبار ثانویه
            self.secondry_product.status = 'secondry_warehouse'
            self.secondry_product.save()

        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.secondry_product.product_name if self.secondry_product else 'محصول ثانویه'} for {self.delivery.receiver_name}"

    class Meta:
        verbose_name = "محصولات ثانویه تحویل افراد"
        verbose_name_plural = "محصولات ثانویه تحویل افراد"
class ProductDeliveryRawMaterial(models.Model):
    delivery = models.ForeignKey(ProductDelivery, on_delete=models.CASCADE, related_name="raw_material_items")
    raw_material = models.ForeignKey(RawMaterialWarehouse, on_delete=models.CASCADE, null=True, blank=True, verbose_name="ماده اولیه")
    quantity = models.IntegerField(verbose_name="تعداد")
    delivery_date = models.DateField(blank=True, null=True, verbose_name="تاریخ تحویل")
    return_date = models.DateField(blank=True, null=True, verbose_name="تاریخ برگشت")
    raw_material_name = models.CharField(max_length=255, verbose_name="ماده اولیه", null=True, blank=True)
    part_number = models.ForeignKey(ProductPart, on_delete=models.CASCADE, null=True, blank=True, verbose_name="پارت کالا")
    item_code = models.ForeignKey(ProductCode, on_delete=models.CASCADE, null=True, blank=True, verbose_name="کد کالا")
    serial_number = models.CharField(max_length=255, blank=True, null=True, verbose_name="شماره سریال")
    user_who_used = models.CharField(blank=True, null=True, max_length=255, verbose_name="استفاده کننده")
    raw_material_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="قیمت ماده اولیه", null=True, blank=True)
    unit = models.CharField(max_length=50, verbose_name="واحد", choices=[
        ('dollar', 'دلار'),
        ('toman', 'تومان')
    ], null=True, blank=True)
    def save(self, *args, **kwargs):
        raw = self.raw_material
        # بررسی اینکه رکورد جدید است یا ویرایش شده
        if self.pk:
            old = ProductDeliveryRawMaterial.objects.get(pk=self.pk)

            if old.raw_material == self.raw_material:
                diff = self.quantity - old.quantity

                if diff > 0:  # افزایش مصرف
                    if raw and raw.quantity >= diff:
                        raw.quantity -= diff
                        raw.save()
                    else:
                        raise ValueError("مقدار جدید بیشتر از موجودی انبار است.")
                elif diff < 0:  # کاهش مصرف
                    if raw:
                        raw.quantity += abs(diff)
                        raw.save()
            else:
                # منبع تغییر کرده
                if old.raw_material:
                    old.raw_material.quantity += old.quantity
                    old.raw_material.save()
                if raw:
                    if raw.quantity >= self.quantity:
                        raw.quantity -= self.quantity
                        raw.save()
                    else:
                        raise ValueError("مقدار وارد شده بیشتر از موجودی انبار است.")
        else:
            # رکورد جدید است
            if raw:
                if raw.quantity >= self.quantity:
                    raw.quantity -= self.quantity
                    raw.save()
                else:
                    raise ValueError("مقدار وارد شده بیشتر از موجودی انبار است.")

        # پر کردن اطلاعات از منبع در صورت خالی بودن
        if raw and not self.raw_material_name:
            self.raw_material_name = raw.piece_name
            self.item_code = raw.item_code
            self.part_number = raw.part_number
            self.raw_material_entry_date = raw.entry_date
            self.raw_material_price = raw.price
            self.unit = raw.unit
            self.serial_number = raw.serial_number

        # بررسی بازگشت مواد اولیه
        if self.pk:  # فقط برای رکوردهای موجود
            old = ProductDeliveryRawMaterial.objects.get(pk=self.pk)
            # اگر تاریخ برگشت اضافه شده و قبلاً خالی بوده
            if self.return_date and not old.return_date:
                # بازگرداندن موجودی به انبار
                if raw:
                    raw.quantity += self.quantity
                    raw.save()
                    # صفر کردن تعداد در این کلاس
                    self.quantity = 0
                # بازگرداندن وضعیت قرنطینه
                if raw and raw.quarantine_reference:
                    raw.quarantine_reference.status = 'transferred'
                    raw.quarantine_reference.save()
            # اگر تاریخ برگشت حذف شده و قبلاً پر بوده
            elif not self.return_date and old.return_date:
                # دوباره کم کردن موجودی از انبار
                if raw and raw.quantity >= self.quantity:
                    raw.quantity -= self.quantity
                    raw.save()
                else:
                    raise ValueError("موجودی انبار کافی نیست.")
                # تغییر وضعیت قرنطینه
                if raw and raw.quarantine_reference:
                    raw.quarantine_reference.status = 'inCompany'
                    raw.quarantine_reference.save()

        # وضعیت قرنطینه (فقط برای رکوردهای جدید)
        if not self.pk and raw and raw.quarantine_reference:     
            raw.quarantine_reference.status = 'inCompany'
            raw.quarantine_reference.save()

        super().save(*args, **kwargs)
    def delete(self, *args, **kwargs):
        if self.raw_material:
            self.raw_material.quantity += self.quantity
            self.raw_material.save()

            # بازگرداندن وضعیت قرنطینه اگر دیگر استفاده نشده باشد
            quarantine_ref = self.raw_material.quarantine_reference
            if quarantine_ref:
                others = ProductDeliveryRawMaterial.objects.filter(
                    raw_material=self.raw_material
                ).exclude(pk=self.pk)

                if not others.exists():
                    quarantine_ref.status = 'transferred'
                    quarantine_ref.save()

        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.raw_material_name} for {self.delivery.receiver_name}"

    class Meta:
        verbose_name = "مواد اولیه تحویل افراد"
        verbose_name_plural = "مواد اولیه تحویل افراد"

class ExternalProductDelivery(models.Model):
    receiver_name = models.CharField(max_length=255, verbose_name="تحویل گیرنده (خارج از شرکت)")
    delivery_date = models.DateField(verbose_name="تاریخ تحویل")
    return_date = models.DateField(blank=True, null=True, verbose_name="تاریخ بازگشت")
    reference_letter = models.BooleanField(default=True,verbose_name="معرفی نامه دارد؟")
    deliverer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="تحویل دهنده"
    )

    def __str__(self):
        return f"{self.receiver_name} - {self.delivery_date}"

    class Meta:
        verbose_name = "امانی شرکت به بیرون"
        verbose_name_plural = "امانی شرکت به بیرون"

class ExternalProductDeliveryProduct(models.Model):
    delivery = models.ForeignKey(ExternalProductDelivery, on_delete=models.CASCADE, related_name="product_items")
    product = models.ForeignKey(ProductWarehouse, on_delete=models.CASCADE, null=True, blank=True, verbose_name="محصول")
    quantity = models.IntegerField(verbose_name="تعداد")
    delivery_date = models.DateField(blank=True, null=True,verbose_name="تاریخ تحویل")
    return_date = models.DateField(blank=True, null=True, verbose_name="تاریخ بازگشت")
    
    def save(self, *args, **kwargs):
        product = self.product
        # بررسی اینکه رکورد جدید است یا ویرایش شده
        if self.pk:
            old = ExternalProductDeliveryProduct.objects.get(pk=self.pk)

            if old.product == self.product:
                diff = self.quantity - old.quantity

                if diff > 0:  # افزایش مصرف
                    if product and product.quantity >= diff:
                        product.quantity -= diff
                        product.save()
                    else:
                        raise ValueError("مقدار جدید بیشتر از موجودی انبار است.")
                elif diff < 0:  # کاهش مصرف
                    if product:
                        product.quantity += abs(diff)
                        product.save()
            else:
                # منبع تغییر کرده
                if old.product:
                    old.product.quantity += old.quantity
                    old.product.save()
                if product:
                    if product.quantity >= self.quantity:
                        product.quantity -= self.quantity
                        product.save()
                    else:
                        raise ValueError("مقدار وارد شده بیشتر از موجودی انبار است.")
        else:
            # رکورد جدید است
            if product:
                if product.quantity >= self.quantity:
                    product.quantity -= self.quantity
                    product.save()
                else:
                    raise ValueError("مقدار وارد شده بیشتر از موجودی انبار است.")

        # بررسی بازگشت محصول
        if self.pk:  # فقط برای رکوردهای موجود
            old = ExternalProductDeliveryProduct.objects.get(pk=self.pk)
            # اگر تاریخ برگشت اضافه شده و قبلاً خالی بوده
            if self.return_date and not old.return_date:
                # بازگرداندن موجودی به انبار محصولات
                if product:
                    product.quantity += self.quantity
                    # تغییر وضعیت به انبار محصولات
                    product.status = 'product_warehouse'
                    product.save()
                    # صفر کردن تعداد در این کلاس
                    self.quantity = 0
            # اگر تاریخ برگشت حذف شده و قبلاً پر بوده
            elif not self.return_date and old.return_date:
                # دوباره کم کردن موجودی از انبار محصولات
                if product and product.quantity >= self.quantity:
                    product.quantity -= self.quantity
                    # تغییر وضعیت به امانی خارجی
                    product.status = 'out_product'
                    product.save()
                else:
                    raise ValueError("موجودی انبار کافی نیست.")
        else:
            # تغییر وضعیت محصول به امانی خارجی (فقط برای رکوردهای جدید)
            if product:
                product.status = 'out_product'
                product.save()

        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        if self.product:
            self.product.quantity += self.quantity
            # بازگرداندن وضعیت محصول به انبار محصولات
            self.product.status = 'product_warehouse'
            self.product.save()

        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.product.product_name if self.product else 'محصول'} for {self.delivery.receiver_name}"

class ExternalProductDeliverySecondryProduct(models.Model):
    delivery = models.ForeignKey(ExternalProductDelivery, on_delete=models.CASCADE, related_name="secondry_items")
    secondry_product = models.ForeignKey(SecondryWarehouse, on_delete=models.CASCADE, null=True, blank=True, verbose_name="محصول ثانویه")
    quantity = models.IntegerField(verbose_name="تعداد")
    delivery_date = models.DateField(blank=True, null=True,verbose_name="تاریخ تحویل")
    return_date = models.DateField(blank=True, null=True, verbose_name="تاریخ بازگشت")
    
    def save(self, *args, **kwargs):
        secondry_product = self.secondry_product
        # بررسی اینکه رکورد جدید است یا ویرایش شده
        if self.pk:
            old = ExternalProductDeliverySecondryProduct.objects.get(pk=self.pk)

            if old.secondry_product == self.secondry_product:
                diff = self.quantity - old.quantity

                if diff > 0:  # افزایش مصرف
                    if secondry_product and secondry_product.quantity >= diff:
                        secondry_product.quantity -= diff
                        secondry_product.save()
                    else:
                        raise ValueError("مقدار جدید بیشتر از موجودی انبار است.")
                elif diff < 0:  # کاهش مصرف
                    if secondry_product:
                        secondry_product.quantity += abs(diff)
                        secondry_product.save()
            else:
                # منبع تغییر کرده
                if old.secondry_product:
                    old.secondry_product.quantity += old.quantity
                    old.secondry_product.save()
                if secondry_product:
                    if secondry_product.quantity >= self.quantity:
                        secondry_product.quantity -= self.quantity
                        secondry_product.save()
                    else:
                        raise ValueError("مقدار وارد شده بیشتر از موجودی انبار است.")
        else:
            # رکورد جدید است
            if secondry_product:
                if secondry_product.quantity >= self.quantity:
                    secondry_product.quantity -= self.quantity
                    secondry_product.save()
                else:
                    raise ValueError("مقدار وارد شده بیشتر از موجودی انبار است.")

        # بررسی بازگشت محصول ثانویه
        if self.pk:  # فقط برای رکوردهای موجود
            old = ExternalProductDeliverySecondryProduct.objects.get(pk=self.pk)
            # اگر تاریخ برگشت اضافه شده و قبلاً خالی بوده
            if self.return_date and not old.return_date:
                # بازگرداندن موجودی به انبار ثانویه
                if secondry_product:
                    secondry_product.quantity += self.quantity
                    # تغییر وضعیت به انبار ثانویه
                    secondry_product.status = 'secondry_warehouse'
                    secondry_product.save()
                    # صفر کردن تعداد در این کلاس
                    self.quantity = 0
            # اگر تاریخ برگشت حذف شده و قبلاً پر بوده
            elif not self.return_date and old.return_date:
                # دوباره کم کردن موجودی از انبار ثانویه
                if secondry_product and secondry_product.quantity >= self.quantity:
                    secondry_product.quantity -= self.quantity
                    # تغییر وضعیت به امانی خارجی
                    secondry_product.status = 'out_product'
                    secondry_product.save()
                else:
                    raise ValueError("موجودی انبار کافی نیست.")
        else:
            # تغییر وضعیت محصول ثانویه به امانی خارجی (فقط برای رکوردهای جدید)
            if secondry_product:
                secondry_product.status = 'out_product'
                secondry_product.save()

        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        if self.secondry_product:
            self.secondry_product.quantity += self.quantity
            self.secondry_product.save()

        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.secondry_product.product_name if self.secondry_product else 'محصول ثانویه'} for {self.delivery.receiver_name}"

class ExternalProductDeliveryRawMaterial(models.Model):
    delivery = models.ForeignKey(ExternalProductDelivery, on_delete=models.CASCADE, related_name="raw_material_items")
    raw_material = models.ForeignKey(RawMaterialWarehouse, on_delete=models.CASCADE, null=True, blank=True, verbose_name="ماده اولیه")
    quantity = models.IntegerField(verbose_name="تعداد")
    delivery_date = models.DateField(blank=True, null=True,verbose_name="تاریخ تحویل")
    return_date = models.DateField(blank=True, null=True, verbose_name="تاریخ بازگشت")
    raw_material_name = models.CharField(max_length=255, verbose_name="ماده اولیه", null=True, blank=True)
    part_number = models.ForeignKey(ProductPart, on_delete=models.CASCADE, null=True, blank=True, verbose_name="پارت کالا")
    item_code = models.ForeignKey(ProductCode, on_delete=models.CASCADE, null=True, blank=True, verbose_name="کد کالا")
    serial_number = models.CharField(max_length=255, blank=True, null=True, verbose_name="شماره سریال")
    
    def save(self, *args, **kwargs):
        raw = self.raw_material
        # بررسی اینکه رکورد جدید است یا ویرایش شده
        if self.pk:
            old = ExternalProductDeliveryRawMaterial.objects.get(pk=self.pk)

            if old.raw_material == self.raw_material:
                diff = self.quantity - old.quantity

                if diff > 0:  # افزایش مصرف
                    if raw and raw.quantity >= diff:
                        raw.quantity -= diff
                        raw.save()
                    else:
                        raise ValueError("مقدار جدید بیشتر از موجودی انبار است.")
                elif diff < 0:  # کاهش مصرف
                    if raw:
                        raw.quantity += abs(diff)
                        raw.save()
            else:
                # منبع تغییر کرده
                if old.raw_material:
                    old.raw_material.quantity += old.quantity
                    old.raw_material.save()
                if raw:
                    if raw.quantity >= self.quantity:
                        raw.quantity -= self.quantity
                        raw.save()
                    else:
                        raise ValueError("مقدار وارد شده بیشتر از موجودی انبار است.")
        else:
            # رکورد جدید است
            if raw:
                if raw.quantity >= self.quantity:
                    raw.quantity -= self.quantity
                    raw.save()
                else:
                    raise ValueError("مقدار وارد شده بیشتر از موجودی انبار است.")

        # پر کردن اطلاعات از منبع در صورت خالی بودن
        if raw and not self.raw_material_name:
            self.raw_material_name = raw.piece_name
            self.item_code = raw.item_code
            self.part_number = raw.part_number
            self.raw_material_entry_date = raw.entry_date
            self.raw_material_price = raw.price
            self.unit = raw.unit
            self.serial_number = raw.serial_number

        # بررسی بازگشت مواد اولیه
        if self.pk:  # فقط برای رکوردهای موجود
            old = ExternalProductDeliveryRawMaterial.objects.get(pk=self.pk)
            # اگر تاریخ برگشت اضافه شده و قبلاً خالی بوده
            if self.return_date and not old.return_date:
                # بازگرداندن موجودی به انبار
                if raw:
                    raw.quantity += self.quantity
                    raw.save()
                    # صفر کردن تعداد در این کلاس
                    self.quantity = 0
                # بازگرداندن وضعیت قرنطینه
                if raw and raw.quarantine_reference:
                    raw.quarantine_reference.status = 'transferred'
                    raw.quarantine_reference.save()
            # اگر تاریخ برگشت حذف شده و قبلاً پر بوده
            elif not self.return_date and old.return_date:
                # دوباره کم کردن موجودی از انبار
                if raw and raw.quantity >= self.quantity:
                    raw.quantity -= self.quantity
                    raw.save()
                else:
                    raise ValueError("موجودی انبار کافی نیست.")
                # تغییر وضعیت قرنطینه
                if raw and raw.quarantine_reference:
                    raw.quarantine_reference.status = 'outCompany'
                    raw.quarantine_reference.save()

        # وضعیت قرنطینه (فقط برای رکوردهای جدید)
        if not self.pk and raw and raw.quarantine_reference:     
            raw.quarantine_reference.status = 'outCompany'
            raw.quarantine_reference.save()

        super().save(*args, **kwargs)
    def delete(self, *args, **kwargs):
        if self.raw_material:
            self.raw_material.quantity += self.quantity
            self.raw_material.save()

            # بازگرداندن وضعیت قرنطینه اگر دیگر استفاده نشده باشد
            quarantine_ref = self.raw_material.quarantine_reference
            if quarantine_ref:
                others = ExternalProductDeliveryRawMaterial.objects.filter(
                    raw_material=self.raw_material
                ).exclude(pk=self.pk)

                if not others.exists():
                    quarantine_ref.status = 'transferred'
                    quarantine_ref.save()

        super().delete(*args, **kwargs)

class ReturnedFromCustomer(models.Model):
    customer_name = models.CharField(max_length=255, verbose_name="نام و نام خانوادگی کارفرما")
    product_name = models.CharField(max_length=255, verbose_name="نام محصول برگشتی")
    product_serial_number = models.CharField(max_length=255, verbose_name="شماره سریال محصول")
    product_part_number = models.CharField(max_length=255, verbose_name="پارت کالا",null=True,blank=True)
    product_item_code = models.CharField(max_length=255, verbose_name="کد کالا",null=True,blank=True)
    return_reason = models.TextField(verbose_name="دلیل برگشت")
    return_date = models.DateField(verbose_name="تاریخ بازگشت")
    received_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="تحویل گیرنده"
    )

    def __str__(self):
        return f"{self.product_name} - {self.customer_name}"

    class Meta:
        verbose_name = "محصول برگشتی شرکت توسط کارفرما"
        verbose_name_plural = "محصول برگشتی شرکت توسط کارفرما"
    
class BorrowedProduct(models.Model):
    product_name = models.CharField(max_length=255, verbose_name="نام محصول")
    serial_number = models.CharField(max_length=255, verbose_name="شماره سریال محصول")
    giver_company = models.CharField(max_length=255, verbose_name="تحویل دهنده (شرکت دیگر)")
    receiver_person = models.CharField(max_length=255, verbose_name="تحویل گیرنده (داخل شرکت)")
    delivery_date = models.DateField(verbose_name="تاریخ تحویل")
    return_date = models.DateField(blank=True, null=True, verbose_name="تاریخ بازگرداندن")

    def __str__(self):
        return f"{self.product_name} - {self.serial_number}"

    class Meta:
        verbose_name = "امانی از شرکت دیگر"
        verbose_name_plural = "امانی از شرکت دیگر"

@receiver(pre_delete, sender=RawMaterialWarehouse)
def update_quarantine_status_on_delete(sender, instance, **kwargs):
    if instance.quarantine_reference:
        quarantine = instance.quarantine_reference
        quarantine.status = "approved"
        quarantine.destination = None
        quarantine.save()

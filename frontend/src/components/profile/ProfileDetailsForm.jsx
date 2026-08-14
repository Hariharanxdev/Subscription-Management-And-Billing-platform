import { useEffect } from "react";
import { useForm, Controller } from "react-hook-form";
import Input from "../ui/Input";
import Select from "../ui/Select";
import Button from "../ui/Button";
import { COUNTRY_OPTIONS } from "../../constants/mockProfile";

const PHONE_PATTERN = {
  value: /^[6-9]\d{9}$/,
  message: "Enter a valid 10-digit mobile number",
};

const PINCODE_PATTERN = {
  value: /^[1-9][0-9]{5}$/,
  message: "Enter a valid 6-digit pincode",
};

/**
 * Pure form component — receives the current values and hands back the
 * submitted values on save. Holds no data of its own beyond the form state,
 * so it stays reusable regardless of where the profile data comes from.
 */
export default function ProfileDetailsForm({ values, onSave, onCancel, saving }) {
  const {
    register,
    handleSubmit,
    control,
    reset,
    formState: { errors, isDirty },
  } = useForm({ defaultValues: values });

  useEffect(() => {
    reset(values);
  }, [values, reset]);

  return (
    <form onSubmit={handleSubmit(onSave)} className="space-y-4" noValidate>
      <Input
        label="Full name"
        placeholder="Your full name"
        error={errors.fullName?.message}
        {...register("fullName", { required: "Full name is required" })}
      />

      <Input
        label="Phone number"
        placeholder="9876543210"
        inputMode="numeric"
        error={errors.phone?.message}
        {...register("phone", { required: "Phone number is required", pattern: PHONE_PATTERN })}
      />

      <Input
        label="Address"
        placeholder="House / street / area"
        error={errors.address?.message}
        {...register("address", { required: "Address is required" })}
      />

      <div className="grid grid-cols-2 gap-4">
        <Input
          label="City"
          placeholder="City"
          error={errors.city?.message}
          {...register("city", { required: "City is required" })}
        />
        <Input
          label="State"
          placeholder="State"
          error={errors.state?.message}
          {...register("state", { required: "State is required" })}
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <Controller
          control={control}
          name="country"
          rules={{ required: "Country is required" }}
          render={({ field }) => (
            <Select label="Country" options={COUNTRY_OPTIONS} error={errors.country?.message} {...field} />
          )}
        />
        <Input
          label="Pincode"
          placeholder="600001"
          inputMode="numeric"
          error={errors.pincode?.message}
          {...register("pincode", { required: "Pincode is required", pattern: PINCODE_PATTERN })}
        />
      </div>

      <div className="flex justify-end gap-3 pt-2">
        <Button type="button" variant="secondary" onClick={onCancel} disabled={saving}>
          Cancel
        </Button>
        <Button type="submit" loading={saving} disabled={!isDirty && !saving}>
          Save changes
        </Button>
      </div>
    </form>
  );
}

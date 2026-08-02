import { useEffect } from "react";
import { useForm } from "react-hook-form";
import Modal from "./Modal";
import Input from "../ui/Input";
import Select from "../ui/Select";
import Button from "../ui/Button";

const BILLING_CYCLES = [
  { value: "monthly", label: "Monthly" },
  { value: "quarterly", label: "Quarterly" },
  { value: "yearly", label: "Yearly" },
];

export default function PlanFormModal({ open, onClose, onSubmit, submitting, initialValues }) {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm({
    defaultValues: {
      plan_name: "",
      description: "",
      price: "",
      billing_cycle: "monthly",
      duration_days: "",
    },
  });

  useEffect(() => {
    if (open) {
      reset(
        initialValues || {
          plan_name: "",
          description: "",
          price: "",
          billing_cycle: "monthly",
          duration_days: "",
        }
      );
    }
  }, [open, initialValues, reset]);

  function submit(values) {
    onSubmit({
      plan_name: values.plan_name,
      description: values.description,
      price: Number(values.price),
      billing_cycle: values.billing_cycle,
      duration_days: Number(values.duration_days),
    });
  }

  return (
    <Modal open={open} onClose={onClose} title={initialValues ? "Edit plan" : "New plan"} size="md">
      <form onSubmit={handleSubmit(submit)} className="space-y-4" noValidate>
        <Input
          label="Plan name"
          placeholder="Pro"
          error={errors.plan_name?.message}
          {...register("plan_name", { required: "Plan name is required" })}
        />
        <Input
          label="Description"
          placeholder="Short description shown to customers"
          error={errors.description?.message}
          {...register("description", { required: "Description is required" })}
        />
        <div className="grid grid-cols-2 gap-4">
          <Input
            label="Price (₹)"
            type="number"
            step="0.01"
            min="0"
            placeholder="499.00"
            error={errors.price?.message}
            {...register("price", {
              required: "Price is required",
              min: { value: 0, message: "Must be positive" },
            })}
          />
          <Input
            label="Duration (days)"
            type="number"
            min="1"
            placeholder="30"
            error={errors.duration_days?.message}
            {...register("duration_days", {
              required: "Duration is required",
              min: { value: 1, message: "At least 1 day" },
            })}
          />
        </div>
        <Select
          label="Billing cycle"
          options={BILLING_CYCLES}
          error={errors.billing_cycle?.message}
          {...register("billing_cycle", { required: true })}
        />
        <Button type="submit" className="w-full" loading={submitting}>
          {initialValues ? "Save changes" : "Create plan"}
        </Button>
      </form>
    </Modal>
  );
}

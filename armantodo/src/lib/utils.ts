import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"
import { useToast } from "@/components/ui/use-toast"
import {toast} from "@/components/ui/use-toast"; 
import {todoFormSchema} from "@/lib/schemas/todo_schema";
import {z} from "zod"
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export const makingFormData = (data: z.infer<typeof todoFormSchema>): FormData => {
  const formData = new FormData();
  Object.entries(data).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
          formData.append(key, value.toString());
      }
  });
  return formData;
}; 
export const toastSuccess = (message: string) => {
  toast({
      title: "Success",
      description: message,
     
  });
}
export const toastError = (message: string) => {
  toast({
      title: "Error",
      description: message,
      
  });
}
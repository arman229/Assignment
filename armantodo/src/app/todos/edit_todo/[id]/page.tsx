"use client";

import { useState, useEffect } from "react";
import { useRouter, useParams } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Form } from "@/components/ui/form";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ReloadIcon } from "@radix-ui/react-icons";
import { toastError, toastSuccess, makingFormData } from "@/lib/utils";
import { LabeledFormInput } from "@/components/my_custom_ui/label_form_input";
import { z } from "zod";
import { todoFormSchema } from "@/lib/schemas/todo_schema";

const EditTodo: React.FC = () => {
    const { id } = useParams();
    const form = useForm<z.infer<typeof todoFormSchema>>({ resolver: zodResolver(todoFormSchema), });
    const [loading, setLoading] = useState<boolean>(false);
    const router = useRouter();

    useEffect(() => {
        fetchTodo();
    }, []);
    const fetchTodo = async () => {
        try {
            const response = await fetch(`/api/todos/get_todos/${id}`);
            if (!response.ok) {
                throw new Error("Failed to fetch todo");
            }
            const data = await response.json();
            form.reset(data);
        } catch (error:any) {
            toastError("Failed to fetch todo"+error.message);
        }
    };

    const onSubmit = async (data: z.infer<typeof todoFormSchema>) => {
        setLoading(true);
        console.log(data)
        const formData = makingFormData(data);
        try {
            const response = await fetch(`/api/todos/edit_todo/${id}`, { method: 'PUT', body: formData });
            if (response.ok) {
                toastSuccess("Todo updated successfully");
                router.push("/todos");
            } else {
                const errorData = await response.json();
                throw new Error(errorData.message || "Failed to update Todo");
            }
        } catch (error: any) {
            toastError(error.message);
        } finally {
            setLoading(false);
        }
    };
    return (
        <Form {...form}>
            <Card className="max-w-md mx-auto mt-10">
                <CardHeader>
                    <CardTitle>Edit Todo</CardTitle>
                </CardHeader>
                <CardContent>
                    <LabeledFormInput
                        label="Title"
                        placeholder="Please enter the todo title"
                        control={form.control}
                        name="title"
                    />
                    <LabeledFormInput
                        label="Description"
                        placeholder="Please enter the todo description"
                        control={form.control}
                        name="description"
                    />
                    <div className="flex justify-end gap-2 mt-4">
                        <Button
                            onClick={() => router.push("/todos")}
                            variant="destructive"
                            disabled={loading}
                        >
                            Cancel
                        </Button>
                        <Button
                            onClick={form.handleSubmit(onSubmit)}
                            disabled={loading}
                        >
                            {loading && (
                                <ReloadIcon className="mr-2 h-4 w-4 animate-spin" />
                            )}
                            Save
                        </Button>
                    </div>
                </CardContent>
            </Card>
        </Form>
    );
};

export default EditTodo;



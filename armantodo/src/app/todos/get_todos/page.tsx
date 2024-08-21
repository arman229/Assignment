"use client";

import useSWR, { mutate } from 'swr';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useRouter } from "next/navigation";
import { Todo } from '@/lib/types';
import { fetcher } from '@/lib/fetcher'


const TodoList: React.FC = () => {
    const { data: todos, error, isLoading } = useSWR<Todo[]>('/api/todos/get_todos', fetcher);
    const router = useRouter();
    return (
        <div className="max-w-md mx-auto mt-10 space-y-4">
            <Button
                onClick={() => router.push("/todos/add_todo")}
                className="text-center"
            >
                Add New Todo
            </Button>

            {isLoading && <div>Loading...</div>}
            {error && <div>Error</div>}
            {todos && (<>
                {todos.map((todo: Todo) => (
                    <Card key={todo.id}>
                        <CardHeader>
                            <CardTitle>{todo.title}</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <p>{todo.description}</p>
                            <div className="flex justify-end gap-2 mt-4">
                                <Button variant="outline" onClick={() => router.push(`/todos/edit_todo/${todo.id}`)} disabled={isLoading}>
                                    edit
                                </Button>
                                <Button variant="destructive" onClick={() => router.push(`/todos/delete_todo/${todo.id}`)} disabled={isLoading}>
                                    Delete
                                </Button>

                            </div>
                        </CardContent>
                    </Card>
                )
                )}
            </>)}



        </div>
    );
};

export default TodoList;

import { NextResponse } from 'next/server';
import { Prisma } from '@prisma/client';
import prisma from'@/lib/prisma'

export async function GET(req: Request, { params }: { params: { id: string } }) {
    const { id } = params;

    try {
        const todo = await prisma.todo.findUnique({
            where: { id: Number(id) },
        });

        if (!todo) {
            return NextResponse.json({ error: 'Todo not found' }, { status: 404 });
        }

        return NextResponse.json(todo);
    } catch (error: any) {
        return NextResponse.json({ error: error.message }, { status: 500 });
    }
}
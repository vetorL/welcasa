import { Edit2, Trash2, ArrowUpDown } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";

export interface Property {
  id: number;
  title: string;
  address: string;
  status: "active" | "inactive";
}

interface PropertyTableProps {
  properties: Property[];
  onEdit: (property: Property) => void;
  onDelete: (id: number) => void;
  onSort: (field: keyof Property) => void;
  sortField: keyof Property | null;
  sortDirection: "asc" | "desc";
}

export const PropertyTable = ({
  properties,
  onEdit,
  onDelete,
  onSort,
  sortField,
  sortDirection,
}: PropertyTableProps) => {
  const getSortIcon = (field: keyof Property) => {
    if (sortField !== field) return <ArrowUpDown className="h-4 w-4 ml-1 opacity-50" />;
    return (
      <ArrowUpDown
        className={`h-4 w-4 ml-1 transition-transform ${
          sortDirection === "desc" ? "rotate-180" : ""
        }`}
      />
    );
  };

  return (
    <div className="rounded-lg border bg-card overflow-hidden">
      <Table>
        <TableHeader>
          <TableRow className="bg-secondary/30">
            <TableHead className="font-bold">
              <button
                onClick={() => onSort("title")}
                className="flex items-center hover:text-foreground transition-colors"
              >
                Título
                {getSortIcon("title")}
              </button>
            </TableHead>
            <TableHead className="font-bold">
              <button
                onClick={() => onSort("address")}
                className="flex items-center hover:text-foreground transition-colors"
              >
                Endereço
                {getSortIcon("address")}
              </button>
            </TableHead>
            <TableHead className="font-bold">
              <button
                onClick={() => onSort("status")}
                className="flex items-center hover:text-foreground transition-colors"
              >
                Status
                {getSortIcon("status")}
              </button>
            </TableHead>
            <TableHead className="text-right font-bold">Ações</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {properties.length === 0 ? (
            <TableRow>
              <TableCell colSpan={4} className="text-center py-8 text-muted-foreground">
                Nenhum imóvel cadastrado
              </TableCell>
            </TableRow>
          ) : (
            properties.map((property) => (
              <TableRow key={property.id} className="hover:bg-secondary/10 transition-colors">
                <TableCell className="font-semibold">{property.title}</TableCell>
                <TableCell>{property.address}</TableCell>
                <TableCell>
                  <Badge 
                    variant={property.status === "active" ? "default" : "secondary"}
                    className={property.status === "active" ? "bg-accent hover:bg-accent/90" : ""}
                  >
                    {property.status === "active" ? "Ativo" : "Inativo"}
                  </Badge>
                </TableCell>
                <TableCell className="text-right">
                  <TooltipProvider>
                    <div className="flex gap-2 justify-end">
                      <Tooltip>
                        <TooltipTrigger asChild>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => onEdit(property)}
                            className="hover:bg-secondary"
                          >
                            <Edit2 className="h-4 w-4" />
                          </Button>
                        </TooltipTrigger>
                        <TooltipContent>
                          <p>Editar imóvel</p>
                        </TooltipContent>
                      </Tooltip>
                      <Tooltip>
                        <TooltipTrigger asChild>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => onDelete(property.id)}
                            className="hover:bg-destructive hover:text-destructive-foreground"
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </TooltipTrigger>
                        <TooltipContent>
                          <p>Remover imóvel</p>
                        </TooltipContent>
                      </Tooltip>
                    </div>
                  </TooltipProvider>
                </TableCell>
              </TableRow>
            ))
          )}
        </TableBody>
      </Table>
    </div>
  );
};
